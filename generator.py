from datetime import datetime, timedelta
from database import get_user, update_gen
import gen_iban_plus

COOLDOWN = timedelta(hours=1)


def can_generate(user_id):
    user = get_user(user_id)

    if not user:
        return False, "USER_NOT_FOUND"

    last = user[3]

    if not last:
        return True, None

    last_dt = datetime.fromisoformat(last)

    if datetime.now() - last_dt >= COOLDOWN:
        return True, None

    return False, str(COOLDOWN - (datetime.now() - last_dt))


def generate(user_id):
    ok, error = can_generate(user_id)

    if not ok:
        return None, error

    iban = gen_iban_plus.generate_iban()

    update_gen(user_id)

    return iban, None
