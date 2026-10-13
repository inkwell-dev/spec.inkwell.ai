// Reference implementation. Adapt to the codebase's conventions (Tailwind, CSS modules, etc.).
// Wordmark is live Geist text: the app already loads Geist, so no outlined SVG is needed in-app.
import * as React from "react";

const NIB = "M11 20.11L6.31 13.58A7 7 0 1 1 17.69 13.58L13 20.11V13.1A2.1 2.1 0 1 0 11 13.1Z";
const NIB_16 = "M10.6 19.55L6.31 13.58A7 7 0 1 1 17.69 13.58L13.4 19.55V11H10.6Z"; // favicon cut: wider slit, no breather hole

export type LogoTone = "color" | "violet" | "slate" | "reversed";
type Theme = "light" | "dark";

const MARK = { light: "#7C3AED", dark: "#8257F0" };
const INK = { light: "#0F172A", dark: "#F8FAFC" };

function colors(tone: LogoTone, theme: Theme) {
  switch (tone) {
    case "violet": return { mark: "#7C3AED", text: "#7C3AED" };
    case "slate": return { mark: "#0F172A", text: "#0F172A" };
    case "reversed": return { mark: "#FFFFFF", text: "#FFFFFF" }; // only on #7C3AED
    default: return { mark: MARK[theme], text: INK[theme] };
  }
}

export function InkwellMark({ size = 24, color = "#7C3AED", ...rest }: { size?: number; color?: string } & React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} aria-hidden="true" {...rest}>
      <path fill={color} d={size <= 16 ? NIB_16 : NIB} />
    </svg>
  );
}

export function InkwellAppIcon({ size = 32, variant = "violet" }: { size?: number; variant?: "violet" | "light" }) {
  const sc = size <= 16 ? 0.72 : size <= 32 ? 0.66 : 0.6;
  const m = 64 * sc, o = (64 - m) / 2, f = m / 24;
  const violet = variant === "violet";
  return (
    <svg viewBox="0 0 64 64" width={size} height={size} role="img" aria-label="Inkwell">
      {violet
        ? <rect width="64" height="64" rx="14" fill="#7C3AED" />
        : <rect x="1" y="1" width="62" height="62" rx="13" fill="#F8FAFC" stroke="#E2E8F0" strokeWidth="2" />}
      <path transform={`translate(${o} ${o}) scale(${f})`} fill={violet ? "#FFFFFF" : "#7C3AED"} d={size <= 16 ? NIB_16 : NIB} />
    </svg>
  );
}

export function InkwellWordmark({ size = 17, color = "#0F172A" }: { size?: number; color?: string }) {
  return (
    <span style={{ fontFamily: "var(--font-geist-sans), Geist, sans-serif", fontWeight: 600, fontSize: size, letterSpacing: "-0.025em", lineHeight: 1, color }}>
      Inkwell
    </span>
  );
}

// Lockup: mark height = 1.2 × font-size, gap = 0.32 × font-size, vertically centered.
export function InkwellLogo({ size = 17, tone = "color", theme = "light" }: { size?: number; tone?: LogoTone; theme?: Theme }) {
  const c = colors(tone, theme);
  return (
    <span role="img" aria-label="Inkwell" style={{ display: "inline-flex", alignItems: "center", gap: size * 0.32 }}>
      <InkwellMark size={Math.round(size * 1.2)} color={c.mark} />
      <InkwellWordmark size={size} color={c.text} />
    </span>
  );
}
