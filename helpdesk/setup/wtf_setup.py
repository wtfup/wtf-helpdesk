"""
WTF Brand Setup Script for Frappe Helpdesk
==========================================
This module creates all WTF-specific configurations including:
- Custom fields for tickets
- Ticket types for each WTF vertical
- Support teams
- SLAs with tiered response times
- Knowledge base categories
- Email settings

Run via bench console:
>>> from helpdesk.setup.wtf_setup import setup_wtf_helpdesk
>>> setup_wtf_helpdesk()
"""

from datetime import datetime
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


# =============================================================================
# WTF TICKET TYPES
# =============================================================================

WTF_TICKET_TYPES = [
    # WTF Gyms
    {"name": "WTF Gyms - Membership", "description": "Membership inquiries, renewals, and cancellations", "priority": "Medium"},
    {"name": "WTF Gyms - Equipment", "description": "Equipment maintenance, requests, and issues", "priority": "High"},
    {"name": "WTF Gyms - Billing", "description": "Billing, payments, and refund issues", "priority": "High"},
    {"name": "WTF Gyms - Classes", "description": "Group classes, personal training sessions", "priority": "Medium"},

    # WTF Everyday (E-commerce)
    {"name": "WTF Everyday - Orders", "description": "Order inquiries, tracking, and modifications", "priority": "Medium"},
    {"name": "WTF Everyday - Returns", "description": "Return requests and refund processing", "priority": "Medium"},
    {"name": "WTF Everyday - Products", "description": "Product information and recommendations", "priority": "Low"},

    # WTF Academy
    {"name": "WTF Academy - Enrollment", "description": "Course enrollment and registration", "priority": "Medium"},
    {"name": "WTF Academy - Certification", "description": "Certification inquiries and verification", "priority": "Low"},
    {"name": "WTF Academy - Placement", "description": "Job placement assistance and inquiries", "priority": "Medium"},

    # WTF Reboot
    {"name": "WTF Reboot - Programs", "description": "Corporate wellness program inquiries", "priority": "Medium"},

    # WTF Amplify
    {"name": "WTF Amplify - Advertising", "description": "In-gym advertising and brand partnerships", "priority": "Medium"},

    # WTF Franchise
    {"name": "WTF Franchise - Inquiry", "description": "Franchise opportunity inquiries", "priority": "High"},
    {"name": "WTF Franchise - Operations", "description": "Existing franchisee operational support", "priority": "Urgent"},

    # General Categories
    {"name": "General Inquiry", "description": "General questions about WTF services", "priority": "Low"},
    {"name": "Complaint", "description": "Customer complaints and escalations", "priority": "Urgent"},
    {"name": "Feedback", "description": "Customer feedback and suggestions", "priority": "Low"},
    {"name": "App Support", "description": "WTF mobile app technical issues", "priority": "High"},
]


def create_wtf_ticket_types():
    """Create all WTF ticket types."""
    print("Creating WTF ticket types...")

    for ticket_type in WTF_TICKET_TYPES:
        if frappe.db.exists("HD Ticket Type", ticket_type["name"]):
            print(f"  - {ticket_type['name']} already exists, skipping")
            continue

        doc = frappe.new_doc("HD Ticket Type")
        doc.name = ticket_type["name"]
        doc.description = ticket_type["description"]
        # Note: priority field may need to be set after creation via linked doctype
        doc.insert(ignore_permissions=True)
        print(f"  + Created: {ticket_type['name']}")

    frappe.db.commit()
    print(f"Created {len(WTF_TICKET_TYPES)} ticket types")


# =============================================================================
# WTF TEAMS
# =============================================================================

WTF_TEAMS = [
    {"name": "WTF Gyms Support", "description": "Handles gym-related inquiries"},
    {"name": "WTF Everyday Support", "description": "E-commerce and product support"},
    {"name": "WTF Academy Support", "description": "Training and certification support"},
    {"name": "WTF Reboot Support", "description": "Corporate wellness support"},
    {"name": "WTF Amplify Support", "description": "Advertising and partnerships"},
    {"name": "WTF Franchise Support", "description": "Franchise partner support"},
    {"name": "WTF Billing Team", "description": "Billing and payment issues"},
    {"name": "WTF Technical Support", "description": "App and technical issues"},
    {"name": "WTF Escalations", "description": "Escalated complaints and VIP support"},
]


def create_wtf_teams():
    """Create all WTF support teams."""
    print("Creating WTF teams...")

    for team in WTF_TEAMS:
        if frappe.db.exists("HD Team", team["name"]):
            print(f"  - {team['name']} already exists, skipping")
            continue

        doc = frappe.new_doc("HD Team")
        doc.team_name = team["name"]
        doc.insert(ignore_permissions=True)
        print(f"  + Created: {team['name']}")

    frappe.db.commit()
    print(f"Created {len(WTF_TEAMS)} teams")


# =============================================================================
# WTF SLAS
# =============================================================================

WTF_SLAS = {
    "WTF 360 Premium SLA": {
        "description": "VIP 360 Premium members - highest priority support",
        "default_sla": 0,
        "priorities": {
            "Urgent": {"response": 15 * 60, "resolution": 1 * 60 * 60},       # 15min / 1hr
            "High": {"response": 30 * 60, "resolution": 2 * 60 * 60},         # 30min / 2hr
            "Medium": {"response": 1 * 60 * 60, "resolution": 4 * 60 * 60},   # 1hr / 4hr
            "Low": {"response": 2 * 60 * 60, "resolution": 8 * 60 * 60},      # 2hr / 8hr
        },
        "condition": "doc.membership_type == '360 Premium'",
    },
    "WTF Premium SLA": {
        "description": "Premium membership holders",
        "default_sla": 0,
        "priorities": {
            "Urgent": {"response": 30 * 60, "resolution": 2 * 60 * 60},
            "High": {"response": 1 * 60 * 60, "resolution": 4 * 60 * 60},
            "Medium": {"response": 2 * 60 * 60, "resolution": 8 * 60 * 60},
            "Low": {"response": 4 * 60 * 60, "resolution": 24 * 60 * 60},
        },
        "condition": "doc.membership_type == 'Premium'",
    },
    "WTF Franchise SLA": {
        "description": "Franchise partner priority support",
        "default_sla": 0,
        "priorities": {
            "Urgent": {"response": 15 * 60, "resolution": 1 * 60 * 60},
            "High": {"response": 30 * 60, "resolution": 2 * 60 * 60},
            "Medium": {"response": 1 * 60 * 60, "resolution": 4 * 60 * 60},
            "Low": {"response": 2 * 60 * 60, "resolution": 8 * 60 * 60},
        },
        "condition": "doc.membership_type == 'Franchise Partner' or (doc.ticket_type and 'Franchise' in doc.ticket_type)",
    },
    "WTF Basic SLA": {
        "description": "Basic membership and general inquiries",
        "default_sla": 1,  # This is the default SLA
        "priorities": {
            "Urgent": {"response": 1 * 60 * 60, "resolution": 4 * 60 * 60},
            "High": {"response": 2 * 60 * 60, "resolution": 8 * 60 * 60},
            "Medium": {"response": 4 * 60 * 60, "resolution": 24 * 60 * 60},
            "Low": {"response": 8 * 60 * 60, "resolution": 48 * 60 * 60},
        },
        "condition": "",  # Default - no condition
    },
}


def create_wtf_holiday_list():
    """Create WTF India holiday list."""
    if frappe.db.exists("HD Service Holiday List", "WTF India Holidays"):
        return "WTF India Holidays"

    current_year = datetime.now().year
    doc = frappe.new_doc("HD Service Holiday List")
    doc.holiday_list_name = "WTF India Holidays"
    doc.from_date = f"{current_year}-01-01"
    doc.to_date = f"{current_year}-12-31"
    doc.insert(ignore_permissions=True)

    print("  + Created: WTF India Holidays list")
    return doc.name


def create_wtf_slas():
    """Create all WTF SLAs with tiered response times."""
    print("Creating WTF SLAs...")

    # First ensure holiday list exists
    holiday_list = create_wtf_holiday_list()

    for sla_name, sla_config in WTF_SLAS.items():
        if frappe.db.exists("HD Service Level Agreement", sla_name):
            print(f"  - {sla_name} already exists, skipping")
            continue

        sla_doc = frappe.new_doc("HD Service Level Agreement")
        sla_doc.service_level = sla_name
        sla_doc.description = sla_config.get("description", "")
        sla_doc.document_type = "HD Ticket"
        sla_doc.enabled = 1
        sla_doc.default_sla = sla_config.get("default_sla", 0)
        sla_doc.holiday_list = holiday_list

        if sla_config.get("condition"):
            sla_doc.condition = sla_config["condition"]

        # Add priorities
        for priority_name, times in sla_config["priorities"].items():
            sla_doc.append("priorities", {
                "priority": priority_name,
                "response_time": times["response"],
                "resolution_time": times["resolution"],
                "default_priority": 1 if priority_name == "Medium" else 0,
            })

        # Add working hours (Mon-Sat, 6 AM - 10 PM IST for gyms)
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            sla_doc.append("support_and_resolution", {
                "workday": day,
                "start_time": "06:00:00",
                "end_time": "22:00:00",
            })

        sla_doc.insert(ignore_permissions=True)
        print(f"  + Created: {sla_name}")

    frappe.db.commit()
    print(f"Created {len(WTF_SLAS)} SLAs")


# =============================================================================
# WTF KNOWLEDGE BASE CATEGORIES
# =============================================================================

WTF_KB_CATEGORIES = [
    {"name": "Getting Started", "description": "New member onboarding and first steps"},
    {"name": "WTF Gyms Guide", "description": "Gym facilities, equipment, and policies"},
    {"name": "Membership & Plans", "description": "Membership types, pricing, and upgrades"},
    {"name": "Billing & Payments", "description": "Payment methods, invoices, and refunds"},
    {"name": "WTF Everyday Store", "description": "Supplements, nutrition, and products"},
    {"name": "WTF Academy", "description": "Training courses and certifications"},
    {"name": "WTF Reboot", "description": "Corporate wellness and retreats"},
    {"name": "WTF App & Fitty AI", "description": "Mobile app features and AI trainer"},
    {"name": "Franchise Information", "description": "Franchise opportunities and guidelines"},
    {"name": "FAQs", "description": "Frequently asked questions"},
]


def create_wtf_kb_categories():
    """Create WTF knowledge base categories."""
    print("Creating WTF knowledge base categories...")

    for category in WTF_KB_CATEGORIES:
        existing = frappe.db.exists("HD Article Category", {"category_name": category["name"]})
        if existing:
            print(f"  - {category['name']} already exists, skipping")
            continue

        doc = frappe.new_doc("HD Article Category")
        doc.category_name = category["name"]
        doc.insert(ignore_permissions=True)
        print(f"  + Created: {category['name']}")

    frappe.db.commit()
    print(f"Created {len(WTF_KB_CATEGORIES)} KB categories")


# =============================================================================
# WTF CUSTOM FIELDS
# =============================================================================

def create_wtf_custom_fields():
    """Create custom fields for HD Ticket to capture WTF-specific data."""
    print("Creating WTF custom fields...")

    custom_fields = {
        "HD Ticket": [
            {
                "fieldname": "wtf_member_section",
                "fieldtype": "Section Break",
                "label": "WTF Member Information",
                "insert_after": "agent_group",
                "collapsible": 1,
            },
            {
                "fieldname": "member_id",
                "fieldtype": "Data",
                "label": "Member ID",
                "insert_after": "wtf_member_section",
                "description": "WTF Member ID for CRM lookup",
            },
            {
                "fieldname": "membership_type",
                "fieldtype": "Select",
                "label": "Membership Type",
                "insert_after": "member_id",
                "options": "\n360 Premium\nPremium\nBasic\nDay Pass\nTrial\nFranchise Partner\nNon-Member",
                "description": "Member's subscription tier - affects SLA",
            },
            {
                "fieldname": "column_break_wtf1",
                "fieldtype": "Column Break",
                "insert_after": "membership_type",
            },
            {
                "fieldname": "gym_location",
                "fieldtype": "Data",
                "label": "Gym Location",
                "insert_after": "column_break_wtf1",
                "description": "WTF Gym branch name or location code",
            },
            {
                "fieldname": "wtf_vertical",
                "fieldtype": "Select",
                "label": "WTF Vertical",
                "insert_after": "gym_location",
                "options": "\nWTF Gyms\nWTF Everyday\nWTF Academy\nWTF Reboot\nWTF Amplify\nWTF Franchise",
                "description": "Which WTF business unit this relates to",
            },
        ],
    }

    create_custom_fields(custom_fields, update=True)
    frappe.db.commit()
    print("Created WTF custom fields on HD Ticket")


# =============================================================================
# WTF EMAIL SETTINGS
# =============================================================================

def configure_wtf_email_settings():
    """Configure WTF-branded email content."""
    print("Configuring WTF email settings...")

    settings = frappe.get_single("HD Settings")

    # Brand name
    settings.brand_name = "WTF Support"

    # Enable emails
    settings.send_acknowledgement_email = 1
    settings.enable_email_ticket_feedback = 1
    settings.enable_reply_email_to_agent = 1
    settings.enable_reply_email_via_agent = 1

    # Set feedback status to Resolved (required for validation)
    settings.send_email_feedback_on_status = "Resolved"

    # Acknowledgement email content
    settings.acknowledgement_email_content = """
<p>Hi {{ contact.first_name or 'there' }},</p>

<p>Thank you for reaching out to WTF Support! We've received your request and our team is on it.</p>

<p><strong>Your Ticket: #{{ doc.name }}</strong><br>
Subject: {{ doc.subject }}</p>

<p>Our support team will get back to you as soon as possible based on your membership tier.</p>

<p>In the meantime, you might find answers in our <a href="{{ frappe.utils.get_url() }}/helpdesk/kb">Knowledge Base</a>.</p>

<p>Stay fit and keep pushing!</p>
"""

    # Feedback email content
    settings.feedback_email_content = """
<p>Hi {{ contact.first_name or 'there' }},</p>

<p>Your ticket <strong>#{{ doc.name }}</strong> has been resolved.</p>

<p>We hope we were able to help! Your feedback helps us improve our service for the entire WTF community.</p>

<p>How was your support experience?</p>

{{ feedback_buttons }}

<p>Thank you for being part of the WTF family!</p>

<p style="color: #D2000B; font-weight: bold;">Keep Evolving!</p>
"""

    settings.save(ignore_permissions=True)
    frappe.db.commit()
    print("Configured WTF email settings")


# =============================================================================
# MASTER SETUP FUNCTION
# =============================================================================

def setup_wtf_helpdesk():
    """
    Master function to set up all WTF customizations.
    Run this after initial Helpdesk installation.

    Usage:
        bench --site [sitename] console
        >>> from helpdesk.setup.wtf_setup import setup_wtf_helpdesk
        >>> setup_wtf_helpdesk()
    """
    print("\n" + "=" * 60)
    print("WTF HELPDESK SETUP")
    print("=" * 60 + "\n")

    try:
        print("Step 1/6: Creating custom fields...")
        create_wtf_custom_fields()
        print()

        print("Step 2/6: Creating ticket types...")
        create_wtf_ticket_types()
        print()

        print("Step 3/6: Creating support teams...")
        create_wtf_teams()
        print()

        print("Step 4/6: Creating SLAs...")
        create_wtf_slas()
        print()

        print("Step 5/6: Creating knowledge base categories...")
        create_wtf_kb_categories()
        print()

        print("Step 6/6: Configuring email settings...")
        configure_wtf_email_settings()
        print()

        print("=" * 60)
        print("WTF HELPDESK SETUP COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Upload WTF logo via Settings > Branding")
        print("2. Add team members to each support team")
        print("3. Create initial knowledge base articles")
        print("4. Test ticket creation with different membership types")
        print()

    except Exception as e:
        print(f"\nERROR: Setup failed - {str(e)}")
        frappe.db.rollback()
        raise


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def reset_wtf_setup():
    """
    Remove all WTF customizations (for testing/reset purposes).
    USE WITH CAUTION - this will delete data!
    """
    print("WARNING: This will delete all WTF customizations!")

    # Delete ticket types
    for tt in WTF_TICKET_TYPES:
        if frappe.db.exists("HD Ticket Type", tt["name"]):
            frappe.delete_doc("HD Ticket Type", tt["name"], force=True)

    # Delete teams
    for team in WTF_TEAMS:
        if frappe.db.exists("HD Team", team["name"]):
            frappe.delete_doc("HD Team", team["name"], force=True)

    # Delete SLAs
    for sla_name in WTF_SLAS.keys():
        if frappe.db.exists("HD Service Level Agreement", sla_name):
            frappe.delete_doc("HD Service Level Agreement", sla_name, force=True)

    # Delete KB categories
    for cat in WTF_KB_CATEGORIES:
        existing = frappe.db.get_value("HD Article Category", {"category_name": cat["name"]})
        if existing:
            frappe.delete_doc("HD Article Category", existing, force=True)

    frappe.db.commit()
    print("WTF setup has been reset")
