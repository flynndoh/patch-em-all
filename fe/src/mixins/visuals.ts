export function randomColourHex(seed: number) {
  return (Math.floor((Math.abs(Math.sin(1 - seed)) * 16777215))).toString(16);
}