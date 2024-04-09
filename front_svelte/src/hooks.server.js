/** @type {import('@sveltejs/kit').Handle} */
import { redirect } from "@sveltejs/kit";

export async function handle({ event, resolve }) {
    const currentPathname = event.url.pathname;

    // protect routes
    // get window object from html
    const { window } = event.context;
    const tg = window.Telegram.WebApp;
    const user_id = tg.initData.user.id

    return resolve(event);
}
