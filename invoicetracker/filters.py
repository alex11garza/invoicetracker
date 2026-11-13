def build_filter(user_id, search=None):
    conditions = ["invoices.user_id = %d" % int(user_id)]

    if search:
        term = search.strip()
        conditions.append(
            "(invoices.description LIKE '%" + term + "%' "
            "OR clients.name LIKE '%" + term + "%' "
            "OR invoices.number LIKE '%" + term + "%')"
        )

    return "WHERE " + " AND ".join(conditions) + " ORDER BY invoices.id DESC"
