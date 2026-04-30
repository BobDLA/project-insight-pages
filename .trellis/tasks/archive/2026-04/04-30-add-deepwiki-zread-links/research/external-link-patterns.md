# External Link Patterns

## Question

How should this repo derive DeepWiki and Zread links for GitHub projects?

## Findings

- DeepWiki repository pages use the pattern
  `https://deepwiki.com/<owner>/<repo>`.
- Zread repository pages accept the pattern `https://zread.ai/<owner>/<repo>`.
- A quick HTTP check against `github/docs` returned HTTP 200 for both derived
  URL shapes.

## Recommendation

Generate DeepWiki and Zread URLs from valid `https://github.com/<owner>/<repo>`
repository URLs. Strip a trailing `.git` suffix from the repository segment.
Omit derived links for URLs that are not GitHub repository URLs.
