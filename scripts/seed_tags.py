"""
Seed script for predefined tag categories.

This script populates the database with the 40 predefined tag categories
and example values for development and testing.
"""

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tcm.database import async_session_maker, engine
from tcm.models import Tag

# Predefined tag data organized by category
PREDEFINED_TAGS = {
    # Organizational (7 tags)
    "organization": [
        "Finance",
        "Operations",
        "Information Technology",
        "Sales & Marketing",
        "Human Resources",
        "Legal & Compliance",
    ],
    "business_unit": [
        "North America",
        "EMEA",
        "APAC",
        "LATAM",
        "Retail Division",
        "Commercial Division",
    ],
    "customer": [
        "Enterprise Clients",
        "SMB",
        "Individual Consumers",
        "Government Agencies",
    ],
    "vendor": [
        "Stripe",
        "PayPal",
        "AWS",
        "Salesforce",
        "Twilio",
    ],
    "program": [
        "Digital Transformation",
        "Cloud Migration",
        "SOX Compliance",
        "GDPR Compliance",
        "System Modernization",
    ],
    "squad": [
        "Platform Team",
        "Frontend Team",
        "Backend Team",
        "QA Team",
        "DevOps Team",
    ],
    "owner": [
        "QA Lead",
        "Test Manager",
        "Product Owner",
        "Engineering Manager",
    ],
    # System/Technical (7 tags)
    "system": [
        "ERP",
        "CRM",
        "HRIS",
        "Payment Gateway",
        "Order Management",
        "Customer Portal",
    ],
    "process": [
        "Order-to-Cash",
        "Procure-to-Pay",
        "Hire-to-Retire",
        "Lead-to-Opportunity",
    ],
    "module": [
        "Authentication",
        "User Management",
        "Reporting",
        "Billing",
        "Inventory",
        "API Integration",
    ],
    "server": [
        "Production",
        "Staging",
        "UAT",
        "QA",
        "Development",
    ],
    "cloud_provider": [
        "AWS",
        "Azure",
        "GCP",
        "On-Premise",
        "Hybrid",
    ],
    "database": [
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "Oracle",
    ],
    "protocol": [
        "HTTP",
        "HTTPS",
        "WebSocket",
        "gRPC",
        "REST",
        "SOAP",
    ],
    # Test-Specific (8 tags)
    "test_type": [
        "Functional",
        "Integration",
        "Performance",
        "Security",
        "Regression",
        "Smoke",
        "Sanity",
    ],
    "test_level": [
        "Unit",
        "Component",
        "Integration",
        "System",
        "Acceptance",
    ],
    "automation_status": [
        "Automated",
        "Manual",
        "Candidate for Automation",
        "Not Automatable",
    ],
    "priority": [
        "Critical",
        "High",
        "Medium",
        "Low",
    ],
    "risk_level": [
        "High Risk",
        "Medium Risk",
        "Low Risk",
    ],
    "test_phase": [
        "Development",
        "System Testing",
        "UAT",
        "Regression",
        "Release Validation",
    ],
    "test_status": [
        "Active",
        "Deprecated",
        "Draft",
        "Under Review",
    ],
    "maintenance_status": [
        "Maintained",
        "Legacy",
        "Sunset",
    ],
    # Platform/Technology (4 tags)
    "platform": [
        "Web",
        "Mobile",
        "Desktop",
        "API",
        "CLI",
    ],
    "browser": [
        "Chrome",
        "Firefox",
        "Safari",
        "Edge",
    ],
    "os": [
        "Windows",
        "Linux",
        "MacOS",
        "iOS",
        "Android",
    ],
    "device_type": [
        "Desktop",
        "Tablet",
        "Mobile",
        "Wearable",
    ],
    # Project Management (4 tags)
    "release": [
        "v1.0",
        "v1.1",
        "v2.0",
        "Q1 2025",
        "Q2 2025",
    ],
    "sprint": [
        "Sprint 1",
        "Sprint 2",
        "Sprint 3",
    ],
    "epic": [
        "User Authentication",
        "Payment Processing",
        "Reporting Dashboard",
    ],
    "feature": [
        "User Login",
        "Password Reset",
        "Two-Factor Authentication",
        "Payment Gateway Integration",
    ],
    # Compliance/Security (3 tags)
    "data_classification": [
        "Public",
        "Internal",
        "Confidential",
        "Restricted",
    ],
    "compliance_requirement": [
        "HIPAA",
        "PCI-DSS",
        "SOX",
        "GDPR",
        "SOC2",
    ],
    "security_level": [
        "Public Access",
        "Authenticated",
        "Role-Based",
        "Admin Only",
    ],
    # Localization/Regional (4 tags)
    "region": [
        "North America",
        "Europe",
        "Asia",
        "South America",
    ],
    "language": [
        "English",
        "Spanish",
        "French",
        "German",
        "Chinese",
    ],
    "locale": [
        "en-US",
        "en-GB",
        "es-ES",
        "fr-FR",
        "de-DE",
    ],
    "timezone": [
        "UTC",
        "EST",
        "PST",
        "CET",
        "JST",
    ],
    # Integration/Dependency (3 tags)
    "integration_point": [
        "Payment Gateway",
        "Email Service",
        "SMS Service",
        "Analytics Platform",
    ],
    "api_version": [
        "v1",
        "v2",
        "v3",
    ],
    "dependency": [
        "External API",
        "Database",
        "Third-party Service",
    ],
}


async def seed_tags():
    """Seed the database with predefined tags."""
    print("Starting tag seeding...")

    async with async_session_maker() as session:
        # Check if tags already exist
        result = await session.execute(select(Tag).limit(1))
        existing = result.scalar_one_or_none()

        if existing:
            print("Tags already exist in database. Skipping seeding.")
            print("To re-seed, delete existing tags first.")
            return

        tags_created = 0

        for category, values in PREDEFINED_TAGS.items():
            for value in values:
                tag = Tag(
                    category=category,
                    value=value,
                    description=f"{value} ({category})",
                    is_predefined=True,
                )
                session.add(tag)
                tags_created += 1

        await session.commit()
        print(f"Successfully created {tags_created} predefined tags")
        print(f"Categories: {len(PREDEFINED_TAGS)}")


async def clear_tags():
    """Clear all tags from the database (for re-seeding)."""
    print("Clearing all tags from database...")

    async with async_session_maker() as session:
        result = await session.execute(select(Tag))
        tags = result.scalars().all()

        for tag in tags:
            await session.delete(tag)

        await session.commit()
        print(f"Deleted {len(tags)} tags")


async def main():
    """Main function to run seeding."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        await clear_tags()
    else:
        await seed_tags()


if __name__ == "__main__":
    asyncio.run(main())
