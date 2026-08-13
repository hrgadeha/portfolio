import frappe


@frappe.whitelist(allow_guest=True)
def submit_lead(lead_name=None, email_id=None, mobile_no=None, company_name=None, message=None):
    """
    Receives the public contact form from the homepage and creates a Lead.
    allow_guest=True is required — visitors submitting this form are not
    logged into the site, so this must be reachable without a session.
    """

    # Basic server-side validation — never trust the client alone
    if not lead_name or not email_id or not message:
        frappe.throw("Name, email, and message are required.")

    lead = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": lead_name,
        "email_id": email_id,
        "mobile_no": mobile_no,
        "company_name": company_name,
        "source": "Website",
    })
    lead.insert(ignore_permissions=True)

    # The message itself is stored as a Comment on the Lead, since "message"
    # isn't a standard Lead field and this avoids depending on a custom field
    # that may not exist on your site.
    lead.add_comment("Comment", text=f"Website inquiry:\n\n{message}")

    frappe.db.commit()

    return {"status": "success", "lead": lead.name}
