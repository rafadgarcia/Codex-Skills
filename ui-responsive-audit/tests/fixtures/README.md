# Browser regression fixture

`regression-site/index.html` deliberately contains the two defect classes added in v0.5.0:

- a person hero whose `object-fit: cover` geometry becomes excessively enlarged at `2560x960`
- a long sticky scene with content crossing fixed top chrome and the viewport bottom

Serve the folder with `scripts/static-serve.mjs`, then run the audit at `wide-low-2560x960`. The findings must include `person-cover-scale-risk` and `sticky-viewport-clipping`.
