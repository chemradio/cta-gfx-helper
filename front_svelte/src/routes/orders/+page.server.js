import { z } from "zod";
import { dispatcherOrdersURL } from "../../config";

export const load = async (event) => {
    const orders = await fetchUserOrders(event);
    return { user: { ...event.locals.user }, orders: orders.reverse() };
};

const videoGFXOrderSchema = z.object({
    request_type: z.enum(["video_auto", "video_files"]),
    quote_enabled: z.bo,
});
const fetchUserOrders = async (event) => {
    const res = await event.fetch(dispatcherOrdersURL, {
        method: "get",
        headers: {
            cookie: `jwt=${event.cookies.get("jwt")}`,
            credentials: "include", // include cookies in the request
        },
    });
    const data = await res.json();
    return data;
};

export const actions = {
    submitVideoGFXOrder: async (event) => {
        console.log("Submit VideoGFX Order action hit");
        const formValues = Object.fromEntries(await event.request.formData());
        const formData = new FormData();

        formData.append("request_type", formValues.request_type);

        let { quote_enabled, audio_enabled } = formValues;
        quote_enabled = quote_enabled === "on" ? true : false;
        audio_enabled = audio_enabled === "on" ? true : false;
        formData.append("quote_enabled", quote_enabled);
        formData.append("audio_enabled", audio_enabled);

        if (quote_enabled) {
            formData.append("quote_text", formValues.quote_text);
            formData.append("quote_author_text", formValues.quote_author_text);
        }

        const { audio_file, foreground_file, background_file, link } =
            formValues;
        if (link.length > 5) {
            formData.append("link", link);
        }
        if (audio_file.size > 0) formData.append("audio_file", audio_file);
        if (foreground_file.size > 0)
            formData.append("foreground_file", foreground_file);
        if (background_file.size > 0)
            formData.append("background_file", background_file);

        const res = await event.fetch(dispatcherOrdersURL, {
            method: "post",
            body: formData,
            headers: {
                cookie: `jwt=${event.cookies.get("jwt")}`,
                credentials: "include", // include cookies in the request
            },
        });
        const responeJSON = await res.json();
        console.log(responeJSON);

        if (res.status == 200) {
            return {
                status: "ok",
                message: "VideoGFX order submitted successfully",
            };
        } else {
            return {
                status: "error",
                message: `Status code ${res.status}: ${responeJSON.detail}`,
            };
        }
    },
};
