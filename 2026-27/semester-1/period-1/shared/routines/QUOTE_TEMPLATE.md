# Daily Quote Pattern

Use the same two-slide quote structure every day.

Keep the opening hook short enough to sit comfortably on one or two large lines. As a rule, aim for about 3-7 words, then add an ellipsis. Put the rest of the quote on the second slide. Quotes should stay roughly within the length of the Day 1 and Day 2 examples; if a quote needs substantially more text, choose a shorter excerpt instead of creating a special layout.

Attribution is always stacked in the same order:

1. Author - always present. Use `Anonymous` if no author is known.
2. Who they are - optional.
3. Book, article, speech, website, resource, or other source - optional.

If line 2 or 3 is not useful, simply omit that span. Do not replace it with a blank line or separator.

Copy this block to the top of the day's `.qmd` file and replace only the bracketed text:

```qmd
# Quote {.quote-hero-slide background-color="#171717"}

::: {.quote-hero-text}
[SHORT OPENING HOOK]...
:::

# Quote {.quote-detail-slide background-color="#171717"}

::: {.quote-hero-text}
[SHORT OPENING HOOK]...
:::

::: {.quote-continuation}
[REST OF QUOTE]
:::

::: {.quote-attribution}
<span class="quote-author">[AUTHOR OR ANONYMOUS]</span>
<span class="quote-role">[WHO THEY ARE - OPTIONAL]</span>
<span class="quote-work">[BOOK / RESOURCE / SOURCE - OPTIONAL]</span>
:::
```

Do not add one-off quote layout classes. The goal is for every day's opening to look the same without CSS changes.
