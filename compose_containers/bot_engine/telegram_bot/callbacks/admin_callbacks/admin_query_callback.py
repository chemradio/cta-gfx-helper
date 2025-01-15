import traceback

from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from py_gfxhelper_lib.user_enums.user_role import UserRole

# from container_interaction.orders import cancel_order
from container_interaction.users import approve_user, block_user, pend_user
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes
from telegram_bot.callbacks.admin_callbacks.list_orders_to_admin import (
    list_10_orders_to_admin,
    list_active_orders_to_admin,
)
from telegram_bot.callbacks.admin_callbacks.list_users_to_admin import (
    list_users_to_admin,
    list_users_to_admin_raw,
)
from telegram_bot.responders.main_responder import Responder


async def admin_query_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    update_dict = update.to_dict()
    callback_query = update_dict.get("callback_query")
    if callback_query:
        await update.callback_query.message.edit_reply_markup(reply_markup=None)
        await update.callback_query.answer(cache_time=180)
        data = update.callback_query.data

        if "approve_" in data:
            applicant_id = int(data.split("approve_")[1])
            await approve_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text.split("\n")[2] + "\nApproved"
            )
            await Responder.register_user.register_approved(applicant_id)
            return True

        if "block_" in data:
            applicant_id = int(data.split("block_")[1])
            await block_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text.split("\n")[2] + "\nBlocked"
            )
            return True

        if "pend_" in data:
            applicant_id = int(data.split("pend_")[1])
            await pend_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text.split("\n")[2] + "\nPending"
            )
            return True

        # if "admin_cancel_order_" in data:
        #     order_id = int(data.split("admin_cancel_order_")[1])
        #     current_message_text = update.callback_query.message.text
        #     raise Exception("Not implemented")
        #     # if await cancel_order(order_id):
        #     #     updated_message_text = current_message_text + "\n\n🛑 CANCELLED"
        #     # else:
        #     #     updated_message_text = (
        #     #         current_message_text + "\n\n🛑 Failed to terminate..."
        #     #     )

        #     # await update.callback_query.edit_message_text(
        #     #     text=updated_message_text, disable_web_page_preview=True
        #     # )
        #     # return True

        # if data == "admin_list_10_orders":
        #     await list_10_orders_to_admin()
        #     return True

        # if data == "admin_list_active_orders":
        #     await list_active_orders_to_admin()
        #     return True

        if data == "admin_list_approved_users":
            await list_users_to_admin(UserPermission.APPROVED)
            return True

        if data == "admin_list_blocked_users":
            await list_users_to_admin(UserPermission.BLOCKED)
            return True

        if data == "admin_list_pending_users":
            await list_users_to_admin(UserPermission.PENDING)
            return True

        if data == "dump_users":
            try:
                await list_users_to_admin_raw()
            except Exception as e:
                print(str(e))
                traceback.print_exc()
            finally:
                return True

        return False
