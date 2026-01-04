from datetime import date, datetime
import calendar

def calculate_age(birth: date, current: date):
    years = current.year - birth.year
    months = current.month - birth.month
    days = current.day - birth.day

    if days < 0:
        # borrow days from previous month
        prev_month = current.month - 1 if current.month > 1 else 12
        prev_year = current.year if current.month > 1 else current.year - 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    return years, months, days

def read_int(prompt: str, min_val: int = None, max_val: int = None):
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError
            return value
        except ValueError:
            rng = ""
            if min_val is not None and max_val is not None:
                rng = f" (between {min_val} and {max_val})"
            print(f"Invalid number{rng}. Please try again.")

def parse_date_input(s: str):
    try:
        # allow YYYY-MM-DD or YYYY/MM/DD
        s = s.strip()
        if not s:
            return None
        for sep in ("-", "/"):
            if sep in s:
                parts = s.split(sep)
                if len(parts) == 3:
                    y, m, d = map(int, parts)
                    return date(y, m, d)
        # fallback try ISO parser
        dt = datetime.fromisoformat(s)
        return dt.date()
    except Exception:
        return None

def main():
    print("Enter your date of birth:")
    by = read_int("  Year (e.g. 1990): ", 1)
    bm = read_int("  Month (1-12): ", 1, 12)
    # determine valid day range for birth month/year
    max_day = calendar.monthrange(by, bm)[1]
    bd = read_int(f"  Day (1-{max_day}): ", 1, max_day)

    birth = date(by, bm, bd)

    cur_input = input("Enter current date as YYYY-MM-DD (press Enter to use today's date): ").strip()
    if cur_input == "":
        current = date.today()
    else:
        parsed = parse_date_input(cur_input)
        if parsed is None:
            print("Couldn't parse the date you entered. Using today's date instead.")
            current = date.today()
        else:
            current = parsed

    if current < birth:
        print("Current date is before birth date. Please check the dates.")
        return

    years, months, days = calculate_age(birth, current)
    print(f"Your age is: {years} years, {months} months, and {days} days.")

if __name__ == "__main__":
    main()
