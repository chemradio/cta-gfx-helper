import { dispatcherOrdersURL } from "../../config";

export const load = async (event) => {
    const orders = await fetchUserOrders(event);
    return { user: { ...event.locals.user }, orders: orders.reverse() };
};

const fetchUserOrders = async (event) => {
    const res = await fetch(dispatcherOrdersURL, {
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
        console.log(formValues);
        return;
        const submitForm = new FormData();

        // Object.entries(await event.request.formData()).forEach((e, i) =>
        //     submitForm.append(...e)
        // );
        console.log([...submitForm.entries()]);

        const res = await event.fetch(dispatcherOrdersURL, {
            method: "post",
            credentials: "include",
            body: submitForm,
        });
        const responeJSON = await res.json();
        console.log(responeJSON);

        if (res.status == 200) {
            return {
                status: "OK",
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
