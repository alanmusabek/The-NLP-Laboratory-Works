import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline  # раскомментируйте в Jupyter

# загрузочные строки оставляю вашими (wget / tar / read_json) — здесь мы начинаем с `lines`

# ---- tokenization: convert 'lines' into space-separated tokens using WordPunctTokenizer
from nltk.tokenize import WordPunctTokenizer
tokenizer = WordPunctTokenizer()

# Example: if you already have `lines` as title + summary, do:
# lines = data.apply(lambda row: row['title'] + ' ; ' + row['summary'].replace("\n", ' '), axis=1).tolist()
# Now replace lines with tokenized, lowercased, space-joined tokens:
lines = [ ' '.join(tokenizer.tokenize(l.lower())).strip() for l in lines ]

# special tokens:
UNK, EOS = "_UNK_", "_EOS_"

from collections import defaultdict, Counter
from tqdm import tqdm

def count_ngrams(lines, n):
    """
    Count occurrences of next-token given (n-1)-token prefix.
    Returns: dict mapping tuple(prefix_tokens) -> Counter({next_token:count})
    """
    counts = defaultdict(Counter)

    for line in lines:
        # tokens are space-separated already
        if isinstance(line, str):
            toks = line.split()
        else:
            toks = list(line)  # defensive
        # append EOS
        toks = toks + [EOS]
        # iterate positions
        for i, tok in enumerate(toks):
            # prefix are previous (n-1) tokens
            if n == 1:
                prefix = tuple()
            else:
                start = i - (n - 1)
                if start < 0:
                    # need padding with UNK
                    pad = [UNK] * (-start)
                    prefix_tokens = pad + toks[:i]
                else:
                    prefix_tokens = toks[start:i]
                # if prefix longer than n-1, take last (n-1)
                prefix = tuple(prefix_tokens[-(n-1):]) if n > 1 else tuple()
                # if prefix shorter pad on left
                if n > 1 and len(prefix) < (n-1):
                    prefix = tuple([UNK] * (n-1 - len(prefix)) + list(prefix))
            counts[prefix][tok] += 1

    return counts

# sanity tests will expect lines to be tokenized; original asserts rely on lowercase tokens like 'p', '=', 'np' etc.

class NGramLanguageModel:
    def __init__(self, lines, n):
        assert n >= 1
        self.n = n
        counts = count_ngrams(lines, self.n)
        self.counts = counts
        self.probs = defaultdict(Counter)
        # normalize
        for prefix, token_counter in counts.items():
            total = float(sum(token_counter.values()))
            self.probs[prefix] = {tok: token_counter[tok] / total for tok in token_counter}

    def get_possible_next_tokens(self, prefix):
        prefix = prefix.split()
        prefix = prefix[max(0, len(prefix) - self.n + 1):]
        prefix = [ UNK ] * (self.n - 1 - len(prefix)) + prefix
        return self.probs.get(tuple(prefix), {})

    def get_next_token_prob(self, prefix, next_token):
        return self.get_possible_next_tokens(prefix).get(next_token, 0.0)

def get_next_token(lm, prefix, temperature=1.0):
    """
    Sample next token from lm given prefix.
    If temperature == 0 -> argmax (deterministic).
    """
    token_probs = lm.get_possible_next_tokens(prefix)
    if not token_probs:
        return EOS  # nothing possible, return EOS to end

    tokens = np.array(list(token_probs.keys()))
    probs = np.array([token_probs[t] for t in tokens], dtype=float)

    if temperature == 0.0:
        # deterministic: pick argmax (break ties arbitrarily)
        idx = int(np.argmax(probs))
        return tokens[idx]
    else:
        # adjust by temperature: use exponent 1/temperature on probabilities
        adjusted = probs ** (1.0 / float(temperature))
        if adjusted.sum() == 0:
            adjusted = np.ones_like(adjusted)
        adjusted = adjusted / adjusted.sum()
        return np.random.choice(tokens, p=adjusted)

def perplexity(lm, lines, min_logprob=np.log(10 ** -50.)):
    """
    Compute corpora-level perplexity using natural logs.
    """
    total_logprob = 0.0
    total_tokens = 0
    for line in lines:
        toks = line.split() + [EOS]
        # iterate tokens
        for i, tok in enumerate(toks):
            # build prefix string (space-separated)
            prefix_tokens = toks[max(0, i - (lm.n - 1)):i]
            prefix_tokens = [UNK] * (lm.n - 1 - len(prefix_tokens)) + prefix_tokens
            prefix_str = ' '.join(prefix_tokens).strip()
            p = lm.get_next_token_prob(prefix_str, tok)
            if p <= 0:
                logp = min_logprob
            else:
                logp = np.log(p)
                if logp < min_logprob:
                    logp = min_logprob
            total_logprob += logp
            total_tokens += 1
    # perplexity
    avg_neg_log = - total_logprob / float(total_tokens)
    return float(np.exp(avg_neg_log))

# ---------- Laplace model is unchanged (you included it) ----------

class LaplaceLanguageModel(NGramLanguageModel):
    def __init__(self, lines, n, delta=1.0):
        self.n = n
        counts = count_ngrams(lines, self.n)
        self.vocab = set(token for token_counts in counts.values() for token in token_counts)
        self.probs = defaultdict(Counter)

        for prefix in counts:
            token_counts = counts[prefix]
            total_count = sum(token_counts.values()) + delta * len(self.vocab)
            self.probs[prefix] = {token: (token_counts[token] + delta) / total_count
                                          for token in token_counts}
    def get_possible_next_tokens(self, prefix):
        token_probs = super().get_possible_next_tokens(prefix)
        missing_prob_total = 1.0 - sum(token_probs.values())
        missing_prob = missing_prob_total / max(1, len(self.vocab) - len(token_probs))
        return {token: token_probs.get(token, missing_prob) for token in self.vocab}

    def get_next_token_prob(self, prefix, next_token):
        token_probs = super().get_possible_next_tokens(prefix)
        if next_token in token_probs:
            return token_probs[next_token]
        else:
            missing_prob_total = 1.0 - sum(token_probs.values())
            missing_prob_total = max(0, missing_prob_total)
            return missing_prob_total / max(1, len(self.vocab) - len(token_probs))


# ---------- Kneser-Ney implementation (recursive, absolute discounting) ----------
class KneserNeyLanguageModel:
    """
    Simple recursive Kneser-Ney implementation with absolute discount delta.
    Works for n >= 1. For n=1 uses continuation probabilities from bigrams.
    """
    def __init__(self, lines, n, delta=0.75):
        assert n >= 1
        self.n = n
        self.delta = float(delta)
        # counts for order n and lower orders
        self.counts = count_ngrams(lines, n)
        # vocabulary: tokens observed as next-token anywhere in counts
        self.vocab = set()
        for c in self.counts.values():
            self.vocab.update(c.keys())
        # build lower-order model recursively
        if n > 1:
            self.lower = KneserNeyLanguageModel(lines, n - 1, delta)
        else:
            # for unigram continuation probs, we need bigram counts
            bigram_counts = count_ngrams(lines, 2)
            # number of distinct bigram types
            total_bigram_types = sum(len(c) for c in bigram_counts.values())
            # count how many distinct left contexts each token has
            left_contexts = Counter()
            for left, ctr in bigram_counts.items():
                for tok in ctr:
                    left_contexts[tok] += 1
            self.continuation_total = total_bigram_types if total_bigram_types > 0 else 1
            self.unigram_cont_prob = {tok: left_contexts[tok] / float(self.continuation_total) for tok in self.vocab}

        # Precompute prefix totals and number of unique continuations for each prefix
        self.prefix_total = {prefix: sum(counter.values()) for prefix, counter in self.counts.items()}
        self.prefix_unique_cont = {prefix: len(counter) for prefix, counter in self.counts.items()}

    def get_possible_next_tokens(self, prefix):
        # returns dict token->prob for tokens in vocab (to make sums to 1)
        token_probs = {}
        prefix_list = prefix.split()
        prefix_list = prefix_list[max(0, len(prefix_list) - self.n + 1):]
        prefix_list = [UNK] * (self.n - 1 - len(prefix_list)) + prefix_list
        prefix_tuple = tuple(prefix_list)

        if self.n == 1:
            # unigram Kneser-Ney: use continuation probability
            # if token unseen -> prob 0
            for tok in self.vocab:
                token_probs[tok] = self.unigram_cont_prob.get(tok, 0.0)
            # normalize (numerical safety)
            s = sum(token_probs.values())
            if s > 0:
                for k in token_probs:
                    token_probs[k] /= s
            return token_probs

        # if prefix observed:
        if prefix_tuple in self.counts:
            cont = self.counts[prefix_tuple]
            total = float(self.prefix_total.get(prefix_tuple, 0.0))
            # discounted probability mass for seen tokens
            for tok in self.vocab:
                c = cont.get(tok, 0)
                discounted = max(c - self.delta, 0.0) / total if total > 0 else 0.0
                token_probs[tok] = discounted
            # backoff weight
            unique = self.prefix_unique_cont.get(prefix_tuple, 0)
            lambda_pref = (self.delta * unique) / total if total > 0 else 1.0
            # get lower order probabilities for continuation
            lower_prefix_tokens = list(prefix_tuple[1:])  # drop first token of prefix to make length n-2
            lower_prefix_str = ' '.join(lower_prefix_tokens).strip()
            lower_probs = self.lower.get_possible_next_tokens(lower_prefix_str)
            # add backoff
            for tok in self.vocab:
                token_probs[tok] = token_probs.get(tok, 0.0) + lambda_pref * lower_probs.get(tok, 0.0)
            # normalize numerically
            s = sum(token_probs.values())
            if s > 0:
                for k in token_probs:
                    token_probs[k] /= s
            return token_probs
        else:
            # unseen prefix -> backoff entirely to lower-order distribution
            lower_prefix_tokens = prefix_list[1:] if len(prefix_list) > 0 else []
            lower_prefix_str = ' '.join(lower_prefix_tokens).strip()
            lower_probs = self.lower.get_possible_next_tokens(lower_prefix_str)
            # ensure domain is self.vocab
            token_probs = {tok: lower_probs.get(tok, 0.0) for tok in self.vocab}
            s = sum(token_probs.values())
            if s > 0:
                for k in token_probs:
                    token_probs[k] /= s
            return token_probs

    def get_next_token_prob(self, prefix, next_token):
        return self.get_possible_next_tokens(prefix).get(next_token, 0.0)

# ------------------------------------------------------------------------------

# If you want to run the tests from your original notebook, the following is a minimal
# snippet showing where to plug things in. (Run the tests in your environment.)

# Example of usage (in your notebook):
# dummy_lines = sorted(lines, key=len)[:100]
# dummy_counts = count_ngrams(dummy_lines, n=3)
# dummy_lm = NGramLanguageModel(dummy_lines, n=3)
# ... etc.

