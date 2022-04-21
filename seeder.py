import random
import uuid
from datetime import datetime, timedelta

from faker import Faker
from flask import current_app

from app.main.model import user, portfolio, property, address, tenant


def seed_data(db):
    """Load initial data into database."""
    fake = Faker('en-GB')

    fake_tenancy_start_date_1 = fake.date_this_decade()
    fake_tenancy_start_date_2 = fake.date_this_decade()
    fake_tenancy_start_date_3 = fake.date_this_decade()
    fake_tenancy_start_date_4 = fake.date_this_decade()
    fake_tenancy_start_date_5 = fake.date_this_decade()
    fake_tenancy_start_date_6 = fake.date_this_decade()
    fake_tenancy_start_date_7 = fake.date_this_decade()
    fake_tenancy_start_date_8 = fake.date_this_decade()
    fake_tenancy_start_date_9 = fake.date_this_decade()
    fake_tenancy_start_date_10 = fake.date_this_decade()
    fake_tenancy_start_date_11 = fake.date_this_decade()

    db.session.remove()  # blat the db
    db.drop_all()  # blat the db
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
        password="test"
    )
    owner_user1.roles = [owner_role, ]

    admin_user = user.User(
        email="marcus_stockton@hotmail.co.uk",
        username="AdminUser",
        first_name="Marcus",
        last_name="Stockton",
        registered_on=datetime.now(),
        public_id=str(uuid.uuid4()),
        date_of_birth=fake.date_of_birth(),
        password="test"
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
                    line_2=fake.street_name(),
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
                        profile_pic=fake.image_url(500, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_1,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_1),
                        profile_pic=fake.image_url(500, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_2,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_2),
                        profile_pic=fake.image_url(500, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=5),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=15),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=25),
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
                        tenancy_start_date=fake_tenancy_start_date_3,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_3),
                        profile_pic=fake.image_url(400, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_4,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_4),
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=55),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=115),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=235),
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
                        profile_pic=fake.image_url(400, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_5,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_5),
                        profile_pic=fake.image_url(400, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_6,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_6),
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=455),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=675),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=755),
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
                        profile_pic=fake.image_url(400, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Miss,
                        first_name=fake.first_name_female(),
                        last_name=fake.last_name_female(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_7,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_7),
                        profile_pic=fake.image_url(400, 400)
                    ),
                    tenant.Tenant(
                        title=tenant.TitleEnum.Mr,
                        first_name=fake.first_name_male(),
                        last_name=fake.last_name_male(),
                        email_address=fake.email(),
                        phone_number=fake.phone_number(),
                        date_of_birth=fake.date_of_birth(),
                        job_title=fake.job(),
                        tenancy_start_date=fake_tenancy_start_date_8,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_8),
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=35),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=25),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=55),
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
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=25),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(hours=123),
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
                        tenancy_start_date=fake_tenancy_start_date_9,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_9),
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=52),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(hours=52),
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
                        tenancy_start_date=fake_tenancy_start_date_10,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_10),
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=43),
                                note=fake.sentence(nb_words=random.randrange(15, 45, 1)),
                            ),
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(hours=42),
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
                        tenancy_start_date=fake_tenancy_start_date_11,
                        tenancy_end_date=fake.date_between_dates(fake_tenancy_start_date_11),
                        profile_pic=fake.image_url(400, 400),
                        notes=[
                            tenant.TenantNote(
                                created_date=datetime.now() - timedelta(minutes=132),
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
