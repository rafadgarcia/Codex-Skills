import assert from "node:assert/strict";
import test from "node:test";

import {
  analyzeCoverGeometry,
  classifyCoverRisk,
  parsePinnedProgress,
  pinnedScrollTarget,
} from "../scripts/audit-geometry.mjs";

test("flags panoramic person cover inflation that makes a portrait feel oversized", () => {
  const geometry = analyzeCoverGeometry({
    naturalWidth: 1672,
    naturalHeight: 940,
    boxWidth: 2560,
    boxHeight: 960,
  });
  assert.ok(geometry.coverInflation > 1.49 && geometry.coverInflation < 1.51);
  assert.ok(geometry.cropYRatio > 0.33 && geometry.cropYRatio < 0.34);
  assert.deepEqual(
    classifyCoverRisk({ geometry, isPerson: true, isHero: true, viewportAspect: 2560 / 960 }),
    { risky: true, severity: "high", reason: "person-cover-scale" },
  );
});

test("keeps matching 16:9 cover geometry below the risk threshold", () => {
  const geometry = analyzeCoverGeometry({
    naturalWidth: 1920,
    naturalHeight: 1080,
    boxWidth: 1920,
    boxHeight: 1080,
  });
  assert.equal(geometry.coverInflation, 1);
  assert.equal(geometry.cropXRatio, 0);
  assert.equal(geometry.cropYRatio, 0);
  assert.equal(
    classifyCoverRisk({ geometry, isPerson: true, isHero: true, viewportAspect: 16 / 9 }).risky,
    false,
  );
});

test("normalizes, clamps, deduplicates, and orders pinned progress samples", () => {
  assert.deepEqual(parsePinnedProgress(".92,0.5,-1,2,.5,invalid"), [0, 0.5, 0.92, 1]);
  assert.deepEqual(parsePinnedProgress("invalid"), [0.08, 0.5, 0.92]);
});

test("maps pinned progress across the scrollable owner range", () => {
  assert.equal(pinnedScrollTarget({ ownerTop: 1200, ownerHeight: 5000, viewportHeight: 1000, progress: 0 }), 1200);
  assert.equal(pinnedScrollTarget({ ownerTop: 1200, ownerHeight: 5000, viewportHeight: 1000, progress: 0.5 }), 3200);
  assert.equal(pinnedScrollTarget({ ownerTop: 1200, ownerHeight: 5000, viewportHeight: 1000, progress: 1 }), 5200);
});
