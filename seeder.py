from app.main.model import user, blacklist, portfolio, property, address, tenant
from datetime import datetime
import uuid


def seed_data(db):
    """Load initial data into database."""
    db.session.remove()  # blatt the db
    db.drop_all()        # blatt the db
    db.create_all()      # create all the tables
    admin_role = user.Role(name="Admin")
    owner_role = user.Role(name="Owner")
    db.session.add_all([owner_role, admin_role])
    owner_user1 = user.User(
        email="test@test.com",
        username="TestUser",
        first_name="Dave",
        last_name="User",
        registered_on=datetime.now(),
        public_id=str(uuid.uuid4()),
        date_of_birth=datetime(1987, 6, 5),
    )
    owner_user1.roles = [owner_role, ]
    admin_user = user.User(
        email="marcus_stockton@hotmail.co.uk",
        username="AdminUser",
        first_name="Marcus",
        last_name="Stockton",
        registered_on=datetime.now(),
        public_id=str(uuid.uuid4()),
        date_of_birth=datetime(1985, 8, 14)
    )
    admin_user.roles = [admin_role, ]
    db.session.add_all([owner_user1, admin_user])
    db.session.commit()

    portfolio1 = portfolio.Portfolio(
        name="Exeter",
        owner_id=owner_role.id,
    )
    portfolio2 = portfolio.Portfolio(
        name="Plymouth",
        owner_id=owner_role.id,
    )
    db.session.add_all([portfolio1, portfolio2])
    db.session.commit()

    address1 = address.Address(
        line_1="54",
        line_2="Wayside Crescent",
        line_3="",
        post_code="EX1 4RE",
        town="",
        city="Exeter",
        property_id=1
    )
    address2 = address.Address(
        line_1="17",
        line_2="The Hoe",
        line_3="",
        post_code="PL5 5YE",
        town="",
        city="Plymouth",
        property_id=2
    )
    db.session.add_all([address1, address2])
    db.session.commit()

    property1 = property.Property(
        address_id=address1.id,
        owner_id=owner_role.id,
        purchase_price=234000,
        purchase_date=datetime(2004, 10, 11),
        monthly_rental_price=675,
        portfolio_id=portfolio1.id
    )
    property2 = property.Property(
        address_id=address2.id,
        owner_id=owner_role.id,
        purchase_price=62000,
        purchase_date=datetime(2011, 4, 6),
        monthly_rental_price=475,
        portfolio_id=portfolio2.id
        )
    db.session.add_all([property1, property2])
    db.session.commit()

    tenant1 = tenant.Tenant(
                title="Mr",
                first_name="Dave",
                last_name="Larson",
                date_of_birth=datetime(1973, 3, 12),
                job_title="Software Engineer",
                tenancy_start_date=datetime(2019, 5, 12),
                profile_pic='tenants/5/ed-warp-art-bfg-space-marines-dark-angels-capitains-05.jpg',
                property_id=1
            )
    tenant2 = tenant.Tenant(
                title="Mrs",
                first_name="Jane",
                last_name="Larson",
                date_of_birth=datetime(1969, 11, 24),
                job_title="Interior Designer",
                tenancy_start_date=datetime(2019, 5, 12),
                property_id=1
            )
    tenant3 = tenant.Tenant(
                title="Mr",
                first_name="Dave",
                last_name="Matthews",
                date_of_birth=datetime(1981, 7, 9),
                job_title="Factory Worker",
                tenancy_start_date=datetime(2020, 9, 7),
                property_id=2
            )
    db.session.add_all([tenant1, tenant2, tenant3])

    tenant1_note = tenant.TenantNote(
        created_date=datetime.now(),
        note="What a dude! So much fun",
        tenant_id=1
    )
    tenant2_note = tenant.TenantNote(
        created_date=datetime.now(),
        note="Seems guarded, but will take care of the place",
        tenant_id=2
    )
    tenant3_note = tenant.TenantNote(
        created_date=datetime.now(),
        note="Lovely guy, enjoys movies and Warhammer. Not one for private do's but looks like he'll keep the place "
             "in good shape.",
        tenant_id=3
    )
    db.session.add_all([tenant1_note, tenant2_note, tenant3_note])
    db.session.commit()
