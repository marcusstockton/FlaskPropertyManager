import random
import uuid
from datetime import datetime

from faker import Faker
from flask import current_app

from app.main.model import user, portfolio, property, address, tenant


def seed_data(db):
    """Load initial data into database."""
    fake = Faker('en-GB')

    fakeTenancyStartDate1 = fake.date_this_decade()
    fakeTenancyStartDate2 = fake.date_this_decade()
    fakeTenancyStartDate3 = fake.date_this_decade()
    fakeTenancyStartDate4 = fake.date_this_decade()
    fakeTenancyStartDate5 = fake.date_this_decade()
    fakeTenancyStartDate6 = fake.date_this_decade()
    fakeTenancyStartDate7 = fake.date_this_decade()
    fakeTenancyStartDate8 = fake.date_this_decade()
    fakeTenancyStartDate9 = fake.date_this_decade()
    fakeTenancyStartDate10 = fake.date_this_decade()
    fakeTenancyStartDate11 = fake.date_this_decade()

    db.session.remove()  # blatt the db
    db.drop_all()  # blatt the db
    db.create_all()  # create all the tables
    admin_role = user.Role(name="Admin")
    owner_role = user.Role(name="Owner")
    db.session.add_all([owner_role, admin_role])
    owner_user1 = user.User(
        email="test@test.com",
        username="TestUser",
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        registered_on=datetime.now(),
        public_id=str(uuid.uuid4()),
        date_of_birth=fake.date_of_birth(),
    )
    owner_user1.roles = [owner_role, ]
    admin_user = user.User(
        email="marcus_stockton@hotmail.co.uk",
        username="AdminUser",
        first_name="Marcus",
        last_name="Stockton",
        registered_on=datetime.now(),
        public_id=str(uuid.uuid4()),
        date_of_birth=fake.date_of_birth()
    )
    admin_user.roles = [admin_role, ]
    db.session.add_all([owner_user1, admin_user])
    db.session.commit()

    portfolio1 = portfolio.Portfolio(
        name=fake.city(),
        owner_id=admin_user.id,
        properties=[
            property.Property(
                address=address.Address(
                    line_1=fake.building_number(),
                    line_2=fake.street_address(),
                    line_3="",
                    post_code=fake.postcode(),
                    town="",
                    city=fake.city()
                ),
                tenants=[
                    tenant.Tenant(
                        title=tenant.TitleEnum.Dr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake.date_this_decade(),
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate1,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate1),
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate2,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate2),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                                tenant_id=1
                            )
                        ]
                    )
                ],
                owner_id=owner_role.id,
                purchase_price=random.randrange(95000, 200000, 1075),
                purchase_date=fake.date_this_century(),
                monthly_rental_price=random.randrange(575, 1000, 100),
            ),
            property.Property(
                address=address.Address(
                    line_1=fake.building_number(),
                    line_2=fake.street_address(),
                    line_3="",
                    post_code=fake.postcode(),
                    town="",
                    city=fake.city(),
                ),
                tenants=[
                    tenant.Tenant(
                        title=tenant.TitleEnum.Dr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake.date_this_decade(),
                        profile_pic='tenants/5/ed-warp-art-bfg-space-marines-dark-angels-capitains-05.jpg',
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate3,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate3),
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate4,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate4),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    )
                ],
                owner_id=owner_role.id,
                purchase_price=random.randrange(95000, 200000, 1075),
                purchase_date=fake.date_this_century(),
                monthly_rental_price=random.randrange(575, 1000, 100),
            )
        ]
    )
    portfolio2 = portfolio.Portfolio(
        name=fake.city(),
        owner_id=owner_role.id,
        properties=[
            property.Property(
                address=address.Address(
                    line_1=fake.building_number(),
                    line_2=fake.street_address(),
                    line_3="",
                    post_code=fake.postcode(),
                    town="",
                    city=fake.city(),
                ),
                tenants=[
                    tenant.Tenant(
                        title=tenant.TitleEnum.Dr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake.date_this_decade(),
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate5,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate5),
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate6,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate6),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    )
                ],
                owner_id=owner_role.id,
                purchase_price=random.randrange(95000, 200000, 1075),
                purchase_date=fake.date_this_century(),
                monthly_rental_price=random.randrange(575, 1000, 100),
            ),
            property.Property(
                address=address.Address(
                    line_1=fake.building_number(),
                    line_2=fake.street_address(),
                    line_3="",
                    post_code=fake.postcode(),
                    town="",
                    city=fake.city(),
                ),
                tenants=[
                    tenant.Tenant(
                        title=tenant.TitleEnum.Dr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake.date_this_decade(),
                        profile_pic='tenants/5/ed-warp-art-bfg-space-marines-dark-angels-capitains-05.jpg',
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate7,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate7),
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate8,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate8),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    )
                ],
                owner_id=owner_role.id,
                purchase_price=random.randrange(95000, 200000, 1075),
                purchase_date=fake.date_this_century(),
                monthly_rental_price=random.randrange(575, 1000, 100),
            )
        ]
    )

    portfolio3 = portfolio.Portfolio(
        name=fake.city(),
        owner_id=owner_role.id,
        properties=[
            property.Property(
                address=address.Address(
                    line_1=fake.building_number(),
                    line_2=fake.street_address(),
                    line_3="",
                    post_code=fake.postcode(),
                    town="",
                    city=fake.city(),
                ),
                tenants=[
                    tenant.Tenant(
                        title=tenant.TitleEnum.Ms,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake.date_this_decade(),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mrs,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate9,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate9),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    )
                ],
                owner_id=owner_role.id,
                purchase_price=random.randrange(95000, 200000, 1075),
                purchase_date=fake.date_this_century(),
                monthly_rental_price=random.randrange(575, 1000, 100),
            ),
            property.Property(
                address=address.Address(
                    line_1=fake.building_number(),
                    line_2=fake.street_address(),
                    line_3="",
                    post_code=fake.postcode(),
                    town="",
                    city=fake.city(),
                ),
                tenants=[
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate10,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate10),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Sir,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fakeTenancyStartDate11,
                        tenancy_end_date=fake.date_between_dates(fakeTenancyStartDate11),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now(),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            )
                        ]
                    )
                ],
                owner_id=owner_role.id,
                purchase_price=random.randrange(95000, 200000, 1075),
                purchase_date=fake.date_this_century(),
                monthly_rental_price=random.randrange(575, 1000, 100),
            )
        ]
    )
    db.session.add_all([portfolio1, portfolio2, portfolio3])
    db.session.commit()
    current_app.logger.info('Database Reseeded!')
