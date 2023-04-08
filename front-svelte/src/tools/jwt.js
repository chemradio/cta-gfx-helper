import jwtDecode from "jwt-decode";

export function decodeJwtToken(token) {
  const decoded = jwtDecode(token);
  return decoded;
}
