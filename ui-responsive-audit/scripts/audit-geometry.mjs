const DEFAULT_PINNED_PROGRESS = [0.08, 0.5, 0.92];

function positiveNumber(value, label) {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) {
    throw new TypeError(`${label} must be a positive number.`);
  }
  return number;
}

export function analyzeCoverGeometry({ naturalWidth, naturalHeight, boxWidth, boxHeight }) {
  const sourceWidth = positiveNumber(naturalWidth, "naturalWidth");
  const sourceHeight = positiveNumber(naturalHeight, "naturalHeight");
  const targetWidth = positiveNumber(boxWidth, "boxWidth");
  const targetHeight = positiveNumber(boxHeight, "boxHeight");
  const coverScale = Math.max(targetWidth / sourceWidth, targetHeight / sourceHeight);
  const containScale = Math.min(targetWidth / sourceWidth, targetHeight / sourceHeight);
  const renderedWidth = sourceWidth * coverScale;
  const renderedHeight = sourceHeight * coverScale;
  const cropXRatio = Math.max(0, 1 - targetWidth / renderedWidth);
  const cropYRatio = Math.max(0, 1 - targetHeight / renderedHeight);

  return {
    coverScale,
    containScale,
    coverInflation: coverScale / containScale,
    renderedWidth,
    renderedHeight,
    cropXRatio,
    cropYRatio,
    visibleFraction: (1 - cropXRatio) * (1 - cropYRatio),
  };
}

export function classifyCoverRisk({ geometry, isPerson = false, isHero = false, viewportAspect = 1 }) {
  const maxCropRatio = Math.max(geometry.cropXRatio, geometry.cropYRatio);
  const personRisk = isPerson && (geometry.coverInflation >= 1.25 || maxCropRatio >= 0.22);
  const panoramicHeroRisk = isHero && viewportAspect >= 2 &&
    (geometry.coverInflation >= 1.3 || maxCropRatio >= 0.25);

  if (personRisk) return { risky: true, severity: "high", reason: "person-cover-scale" };
  if (panoramicHeroRisk) return { risky: true, severity: "high", reason: "panoramic-cover-scale" };
  if (isHero && (geometry.coverInflation >= 1.45 || maxCropRatio >= 0.34)) {
    return { risky: true, severity: "medium", reason: "hero-cover-scale" };
  }
  return { risky: false, severity: null, reason: null };
}

export function parsePinnedProgress(value, fallback = DEFAULT_PINNED_PROGRESS) {
  const values = Array.isArray(value)
    ? value
    : typeof value === "string"
      ? value.split(",")
      : fallback;
  const normalized = [...new Set(values
    .map((entry) => Number(entry))
    .filter((entry) => Number.isFinite(entry))
    .map((entry) => Math.min(1, Math.max(0, entry))))]
    .sort((a, b) => a - b);
  return normalized.length ? normalized : [...fallback];
}

export function pinnedScrollTarget({ ownerTop, ownerHeight, viewportHeight, progress }) {
  const top = Number(ownerTop);
  const height = positiveNumber(ownerHeight, "ownerHeight");
  const viewport = positiveNumber(viewportHeight, "viewportHeight");
  const normalizedProgress = Math.min(1, Math.max(0, Number(progress) || 0));
  return Math.max(0, top + Math.max(0, height - viewport) * normalizedProgress);
}
