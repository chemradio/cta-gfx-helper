import { redirect } from "@sveltejs/kit";
import { z } from "zod";
import { dispatcherLoginURL, dispatcherRegisterURL } from "../../config.js";

export const load = async (event, resolve) => {
    // remove current cookie if present
    event.cookies.delete("jwt");
    try {
        await event.fetch(dispatcherLoginURL, {
            method: "DELETE",
        });
    } catch (e) {
        console.log("Logout server reports error: ", e);
    }
    event.locals.user = {};
    return {
        status: "ok",
        message: "Log in or Register to continue",
    };
};

const loginSchema = z.object({
    login_email: z
        .string({ required_error: "Email must be provided" })
        .min(5, { message: "Too short" })
        .max(64, { message: "Too Long" })
        .email({ message: "Invalid email" }),
    login_password: z
        .string({ required_error: "Email must be provided" })
        .min(5, { message: "Too short" })
        .max(64, { message: "Too Long" }),
});

const registerSchema = z.object({
    register_email: z
        .string({ required_error: "Email must be provided" })
        .min(5, { message: "Too short" })
        .max(64, { message: "Too Long" })
        .email({ message: "Invalid email" }),
    register_password: z
        .string({ required_error: "Password must be provided" })
        .min(5, { message: "Too short" })
        .max(64, { message: "Too Long" }),
    register_passphrase: z.string({
        required_error: "Passphrase must be provided",
    }),
});

export const actions = {
    login: async (event) => {
        // console.log("login hi");
        // const resp = await fetch("https://dummyjson.com/products/1");
        // const respJSON = await resp.json();
        // return { from: "login", ...respJSON };

        console.log("Login action hit");
        console.log("dispatcherLoginURL", dispatcherLoginURL);

        let jwt = event.cookies.get("jwt");

        const formData = Object.fromEntries(await event.request.formData());

        // validate form
        try {
            const result = loginSchema.parse(formData);
        } catch (err) {
            return {
                status: "error",
                message: "Check the form and try again",
                data: formData.email,
                errors: err.flatten().fieldErrors,
            };
        }

        const { login_email, login_password } = formData;

        const loginFormData = new FormData();
        loginFormData.append("email", login_email);
        loginFormData.append("password", login_password);

        const res = await fetch(dispatcherLoginURL, {
            method: "POST",
            body: loginFormData,
            headers: {
                cookie: `jwt=${jwt}`,
                credentials: "include", // include cookies in the request
            },
        });

        if (res.status === 200) {
            // authenticated. attach new cookie
            jwt = res.headers.get("set-cookie").split('"')[1];
            event.cookies.set("jwt", jwt, {
                path: "/",
                secure: false,
                maxAge: 60 * 60 * 24 * 30,
            });
            throw redirect(302, "/orders");
        } else {
            // remove current cookie if present
            event.cookies.delete("jwt");
            return { status: "error", message: "Bad credentials" };
        }
    },

    register: async (event) => {
        // console.log("register hi");
        // const resp = await fetch("https://dummyjson.com/products/1");
        // const respJSON = await resp.json();
        // return { from: "register", ...respJSON };

        console.log("Register action hit!");
        console.log("dispatcherRegisterURL", dispatcherRegisterURL);
        const formData = Object.fromEntries(await event.request.formData());

        // validate form
        console.log("Form validation started");
        try {
            const result = registerSchema.parse(formData);
        } catch (err) {
            return {
                status: "error",
                message: "Check the form and try again",
                data: formData.email,
                errors: err.flatten().fieldErrors,
            };
        }

        const { register_email, register_password, register_passphrase } =
            formData;

        console.log("Creating form data");
        const registerFormData = new FormData();
        registerFormData.append("email", register_email);
        registerFormData.append("password", register_password);
        registerFormData.append("passphrase", register_passphrase);

        console.log("Pre fetch to dispatcher");
        const res = await fetch(dispatcherRegisterURL, {
            method: "POST",
            body: registerFormData,
        });

        if (res.status === 200) {
            // authenticated. attach new cookie. redirect to home
            console.log("Fetch status 200! Trying to add cookie");
            console.log(
                "Set cookie from the response headers:",
                res.headers.get("set-cookie")
            );
            console.log(
                "Atttaching split part:",
                res.headers.get("set-cookie").split('"')[1]
            );
            event.cookies.set(
                "jwt",
                res.headers.get("set-cookie").split('"')[1],
                {
                    path: "/",
                    // httpOnly: true,
                    // sameSite: "none",
                    secure: false,
                    maxAge: 60 * 60 * 24 * 30,
                }
            );
            console.log("Cookie added. Throwing redirect");
            throw redirect(302, "/orders");
        } else {
            const responseJSON = await res.json();
            return {
                status: "error",
                message: responseJSON.detail,
            };
        }
    },
};
