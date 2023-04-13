/** @type {import('@sveltejs/kit').Handle} */
import { redirect } from "@sveltejs/kit";
import { decodeJwtToken } from "./tools/jwt";

export async function handle({ event, resolve }) {
    const currentPathname = event.url.pathname;
    const jwt = event.cookies.get("jwt");

    // protect routes
    if (currentPathname === "/orders" && !jwt) throw redirect(307, "/login");

    let userData = {};
    if (jwt) {
        userData = decodeJwtToken(jwt);
    }
    event.locals.user = userData;

    return resolve(event);
}
