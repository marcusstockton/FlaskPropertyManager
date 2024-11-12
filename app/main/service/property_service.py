"""User Service for interacting with users"""

import datetime
from http import HTTPStatus
from typing import List

from bleach import clean
from flask import current_app
from sqlalchemy.orm import lazyload
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest

from app.main import db
from app.main.model.address import Address
from app.main.model.portfolio import Portfolio
from app.main.model.property import Property
from app.main.model.property_image import PropertyImages


def get_all_properties_for_portfolio(user, portfolio_id) -> List[Property]:
    """Gets all properties for the portfolio id"""
    current_app.logger.info("Getting all properties for portfolio_id %s", portfolio_id)
    if user.admin:
        return (
            Property.query.options(lazyload(Property.tenants))
            .filter_by(portfolio_id=portfolio_id)
            .all()
        )
    return (
        Property.query.options(lazyload(Property.tenants))
        .filter(Portfolio.owner == user)
        .filter_by(portfolio_id=portfolio_id)
        .all()
    )


def save_new_property(portfolio_id, data):
    """Adds new property to portfolio"""
    portfolio: Portfolio | None = Portfolio.query.filter_by(id=portfolio_id).first()

    if portfolio is None:
        current_app.logger.error("No portfolio found portfolio_id %s", portfolio_id)
        raise NotFound("No portfolio found")

    if data["address"]:
        # create address
        new_address = Address(
            line_1=clean(data["address"]["line_1"]),
            line_2=data["address"].get("line_2", None),
            line_3=data["address"].get("line_3", None),
            post_code=clean(data["address"]["post_code"]),
            town=data["address"].get("town", None),
            city=data["address"].get("city", None),
        )
        current_app.logger.info("Created address")
        new_property = Property(
            portfolio_id=portfolio_id,
            purchase_price=data["purchase_price"],
            purchase_date=datetime.datetime.strptime(data["purchase_date"], "%Y-%m-%d"),
            monthly_rental_price=data["monthly_rental_price"],
            sold_date=None,
        )
        current_app.logger.info("Created property")

        new_property.address = new_address
        portfolio.properties.append(new_property)
        try:
            save_changes(portfolio)
            response_object = {
                "status": "success",
                "message": "Successfully created property.",
                "data": {"id": new_property.id},
            }
            return response_object, HTTPStatus.CREATED
        except Exception as ex:
            raise InternalServerError(f"Unable to save new Property. {ex}") from ex


def get_property_by_id(user, portfolio_id, property_id) -> Property:
    """Gets a property by its ID"""
    try:
        current_app.logger.info(
            "Getting properties with portfolio_id %s property_id %s",
            portfolio_id,
            property_id,
        )
        if user.admin:
            return Property.query.filter_by(
                portfolio_id=portfolio_id, id=property_id
            ).one()
        else:
            query = (
                db.session.query(Property)
                .filter(Portfolio.owner == user)
                .filter(Portfolio.id == portfolio_id)
                .filter(Property.id == property_id)
                .one()
            )
            return query

    except MultipleResultsFound as err:
        current_app.logger.error(
            "Multiple properties found... portfolio_id %s property_id %s",
            portfolio_id,
            property_id,
        )
        print(err)
        raise BadRequest(
            f"Multiple properties found... portfolio_id {portfolio_id}, property_id {property_id}"
        ) from err
    except NoResultFound as err:
        current_app.logger.error(
            "No properties found with portfolio_id %s, property_id %s, user_id %s",
            portfolio_id,
            property_id,
            user.id,
        )
        print(err)
        raise NotFound(
            f"No properties found with portfolio_id {portfolio_id}, property_id {property_id}, user_id {user.id}"
        ) from err


def add_images_to_property(portfolio_id, property_id, images):
    """Adds image(s) to property"""
    try:
        property_obj: Property = Property.query.filter_by(
            portfolio_id=portfolio_id, id=property_id
        ).one()
    except MultipleResultsFound as err:
        raise BadRequest("Multiple Records Found") from err
    except NoResultFound as err:
        raise NotFound(f"No property found with id {property_id}") from err

    new_images = []
    for image in images:
        new_images.append(
            PropertyImages(
                property_id=property_id,
                property=property_obj,
                image=image.image,
                file_name=image.file_name,
            )
        )

    save_all_changes(new_images)
    return property_obj, HTTPStatus.CREATED


def save_changes(data) -> None:
    """Save Changes"""
    db.session.add(data)
    db.session.commit()


def save_all_changes(data) -> None:
    """Save all Changes"""
    db.session.add_all(data)
    db.session.commit()
