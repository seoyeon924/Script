import { Renderer, Program, Mesh, Color, Triangle } from 'https://esm.sh/ogl@1.0.8';

const vertexShader = `
attribute vec2 uv;
attribute vec2 position;
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 0, 1);
}
`;

const fragmentShader = `
precision highp float;

uniform float uTime;
uniform vec3 uResolution;
uniform vec2 uFocal;
uniform vec2 uRotation;
uniform float uStarSpeed;
uniform float uDensity;
uniform float uHueShift;
uniform float uSpeed;
uniform vec2 uMouse;
uniform float uGlowIntensity;
uniform float uSaturation;
uniform bool uMouseRepulsion;
uniform float uTwinkleIntensity;
uniform float uRotationSpeed;
uniform float uRepulsionStrength;
uniform float uMouseActiveFactor;
uniform float uAutoCenterRepulsion;
uniform bool uTransparent;

varying vec2 vUv;

#define NUM_LAYER 4.0
#define STAR_COLOR_CUTOFF 0.2
#define MAT45 mat2(0.7071, -0.7071, 0.7071, 0.7071)
#define PERIOD 3.0

float Hash21(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float vnoise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  float a = Hash21(i);
  float b = Hash21(i + vec2(1.0, 0.0));
  float c = Hash21(i + vec2(0.0, 1.0));
  float d = Hash21(i + vec2(1.0, 1.0));
  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
  float v = 0.0;
  float a = 0.5;
  for (int i = 0; i < 5; i++) {
    v += a * vnoise(p);
    p *= 2.0;
    a *= 0.5;
  }
  return v;
}

vec3 nebula(vec2 uv) {
  float t = uTime * 0.02;
  float n1 = fbm(uv * 1.2 + vec2(t * 0.3, t * 0.1));
  float n2 = fbm(uv * 1.5 + vec2(-t * 0.2, t * 0.15) + 100.0);
  float n3 = fbm(uv * 0.8 + vec2(t * 0.1, -t * 0.25) + 200.0);
  vec3 purple = vec3(0.35, 0.05, 0.55) * smoothstep(0.3, 0.7, n1);
  vec3 blue = vec3(0.08, 0.1, 0.45) * smoothstep(0.35, 0.75, n2);
  vec3 gold = vec3(0.5, 0.25, 0.05) * smoothstep(0.5, 0.85, n3);
  vec3 pink = vec3(0.45, 0.08, 0.3) * smoothstep(0.55, 0.8, n1 * n2);
  vec3 col = purple + blue + gold + pink;
  float dist = length(uv);
  col *= smoothstep(3.0, 0.5, dist) * 0.35;
  return col;
}

float tri(float x) { return abs(fract(x) * 2.0 - 1.0); }
float tris(float x) { float t = fract(x); return 1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0)); }
float trisn(float x) { float t = fract(x); return 2.0 * (1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0))) - 1.0; }

vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

float Star(vec2 uv, float flare) {
  float d = length(uv);
  float m = (0.05 * uGlowIntensity) / d;
  float rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));
  m += rays * flare * uGlowIntensity;
  uv *= MAT45;
  rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));
  m += rays * 0.3 * flare * uGlowIntensity;
  m *= smoothstep(1.0, 0.2, d);
  return m;
}

vec3 StarLayer(vec2 uv) {
  vec3 col = vec3(0.0);
  vec2 gv = fract(uv) - 0.5;
  vec2 id = floor(uv);
  for (int y = -1; y <= 1; y++) {
    for (int x = -1; x <= 1; x++) {
      vec2 offset = vec2(float(x), float(y));
      vec2 si = id + vec2(float(x), float(y));
      float seed = Hash21(si);
      float size = fract(seed * 345.32);
      float glossLocal = tri(uStarSpeed / (PERIOD * seed + 1.0));
      float flareSize = smoothstep(0.9, 1.0, size) * glossLocal;
      vec3 base = vec3(1.0);
      vec2 pad = vec2(tris(seed * 34.0 + uTime * uSpeed / 10.0), tris(seed * 38.0 + uTime * uSpeed / 30.0)) - 0.5;
      float star = Star(gv - offset - pad, flareSize);
      vec3 color = base;
      float twinkle = trisn(uTime * uSpeed + seed * 6.2831) * 0.5 + 1.0;
      twinkle = mix(1.0, twinkle, uTwinkleIntensity);
      star *= twinkle;
      col += star * size * color;
    }
  }
  return col;
}

void main() {
  vec2 focalPx = uFocal * uResolution.xy;
  vec2 uv = (vUv * uResolution.xy - focalPx) / uResolution.y;
  vec2 mouseNorm = uMouse - vec2(0.5);
  if (uAutoCenterRepulsion > 0.0) {
    vec2 centerUV = vec2(0.0, 0.0);
    float centerDist = length(uv - centerUV);
    vec2 repulsion = normalize(uv - centerUV) * (uAutoCenterRepulsion / (centerDist + 0.1));
    uv += repulsion * 0.05;
  } else if (uMouseRepulsion) {
    vec2 mousePosUV = (uMouse * uResolution.xy - focalPx) / uResolution.y;
    float mouseDist = length(uv - mousePosUV);
    vec2 repulsion = normalize(uv - mousePosUV) * (uRepulsionStrength / (mouseDist + 0.1));
    uv += repulsion * 0.05 * uMouseActiveFactor;
  } else {
    vec2 mouseOffset = mouseNorm * 0.1 * uMouseActiveFactor;
    uv += mouseOffset;
  }
  float autoRotAngle = uTime * uRotationSpeed;
  mat2 autoRot = mat2(cos(autoRotAngle), -sin(autoRotAngle), sin(autoRotAngle), cos(autoRotAngle));
  uv = autoRot * uv;
  uv = mat2(uRotation.x, -uRotation.y, uRotation.y, uRotation.x) * uv;
  vec3 col = vec3(0.0);
  for (float i = 0.0; i < 1.0; i += 1.0 / NUM_LAYER) {
    float depth = fract(i + uStarSpeed * uSpeed);
    float scale = mix(20.0 * uDensity, 0.5 * uDensity, depth);
    float fade = depth * smoothstep(1.0, 0.9, depth);
    col += StarLayer(uv * scale + i * 453.32) * fade;
  }
  float alpha = length(col);
  alpha = smoothstep(0.15, 0.85, alpha);
  alpha = min(alpha, 1.0);
  gl_FragColor = vec4(col, alpha);
}
`;

export function initGalaxy(containerId) {
  const focal = [0.5, 0.5];
  const rotation = [1.0, 0.0];
  const starSpeed = 0.5;
  const density = 1;
  const hueShift = 270;
  const speed = 0.8;
  const glowIntensity = 0.25;
  const saturation = 0.65;
  const mouseRepulsion = true;
  const repulsionStrength = 2;
  const twinkleIntensity = 0.3;
  const rotationSpeed = 0.05;
  const autoCenterRepulsion = 0;

  const ctn = document.getElementById(containerId);
  if (!ctn) return;

  const targetMouse = { x: 0.5, y: 0.5 };
  const smoothMouse = { x: 0.5, y: 0.5 };
  let targetActive = 0.0;
  let smoothActive = 0.0;

  const renderer = new Renderer({ alpha: true, premultipliedAlpha: false });
  const gl = renderer.gl;
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  gl.clearColor(0, 0, 0, 0);

  let program;

  function resizeGalaxy() {
    renderer.setSize(ctn.offsetWidth, ctn.offsetHeight);
    if (program) {
      program.uniforms.uResolution.value = new Color(
        gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height
      );
    }
  }
  window.addEventListener('resize', resizeGalaxy, false);
  resizeGalaxy();

  const geometry = new Triangle(gl);
  program = new Program(gl, {
    vertex: vertexShader,
    fragment: fragmentShader,
    uniforms: {
      uTime: { value: 0 },
      uResolution: { value: new Color(gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height) },
      uFocal: { value: new Float32Array(focal) },
      uRotation: { value: new Float32Array(rotation) },
      uStarSpeed: { value: starSpeed },
      uDensity: { value: density },
      uHueShift: { value: hueShift },
      uSpeed: { value: speed },
      uMouse: { value: new Float32Array([0.5, 0.5]) },
      uGlowIntensity: { value: glowIntensity },
      uSaturation: { value: saturation },
      uMouseRepulsion: { value: mouseRepulsion },
      uTwinkleIntensity: { value: twinkleIntensity },
      uRotationSpeed: { value: rotationSpeed },
      uRepulsionStrength: { value: repulsionStrength },
      uMouseActiveFactor: { value: 0.0 },
      uAutoCenterRepulsion: { value: autoCenterRepulsion },
      uTransparent: { value: true }
    }
  });

  const mesh = new Mesh(gl, { geometry, program });

  function updateGalaxy(t) {
    requestAnimationFrame(updateGalaxy);
    program.uniforms.uTime.value = t * 0.001;
    program.uniforms.uStarSpeed.value = (t * 0.001 * starSpeed) / 10.0;
    const lerpFactor = 0.05;
    smoothMouse.x += (targetMouse.x - smoothMouse.x) * lerpFactor;
    smoothMouse.y += (targetMouse.y - smoothMouse.y) * lerpFactor;
    smoothActive += (targetActive - smoothActive) * lerpFactor;
    program.uniforms.uMouse.value[0] = smoothMouse.x;
    program.uniforms.uMouse.value[1] = smoothMouse.y;
    program.uniforms.uMouseActiveFactor.value = smoothActive;
    renderer.render({ scene: mesh });
  }
  requestAnimationFrame(updateGalaxy);
  ctn.appendChild(gl.canvas);

  ctn.addEventListener('mousemove', (e) => {
    const rect = ctn.getBoundingClientRect();
    targetMouse.x = (e.clientX - rect.left) / rect.width;
    targetMouse.y = 1.0 - (e.clientY - rect.top) / rect.height;
    targetActive = 1.0;
  });
  ctn.addEventListener('mouseleave', () => { targetActive = 0.0; });
}
