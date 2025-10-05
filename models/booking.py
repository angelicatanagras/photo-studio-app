from datetime import datetime, date
from ..database import fetch_one, fetch_all, execute_query


class ServiceCategory:
    """Service category model for grouping services."""

    def __init__(self, category_dict):
        """Initialize service category from database dictionary."""
        if category_dict:
            self.id = category_dict.get('id')
            self.category_name = category_dict.get('category_name')
            self.description = category_dict.get('description')

    @staticmethod
    def get_by_id(category_id):
        """Get service category by ID."""
        category_data = fetch_one(
            "SELECT * FROM service_categories WHERE id = %s",
            (category_id,)
        )
        return ServiceCategory(category_data) if category_data else None

    @staticmethod
    def get_all():
        """Get all service categories."""
        categories_data = fetch_all("SELECT * FROM service_categories")
        return [ServiceCategory(c) for c in categories_data]

    @staticmethod
    def create(category_name, description=None):
        """Create a new service category."""
        category_id = execute_query(
            "INSERT INTO service_categories (category_name, description) VALUES (%s, %s)",
            (category_name, description)
        )
        return ServiceCategory.get_by_id(category_id)

    def __repr__(self):
        return f'<ServiceCategory {self.category_name}>'


class Service:
    """Service model for photographer services."""

    def __init__(self, service_dict):
        """Initialize service from database dictionary."""
        if service_dict:
            self.id = service_dict.get('id')
            self.photographer_id = service_dict.get('photographer_id')
            self.name = service_dict.get('name')
            self.description = service_dict.get('description')
            self.service_category_id = service_dict.get('service_category_id')
            self.created_at = service_dict.get('created_at')

    @staticmethod
    def get_by_id(service_id):
        """Get service by ID."""
        service_data = fetch_one(
            "SELECT * FROM services WHERE id = %s",
            (service_id,)
        )
        return Service(service_data) if service_data else None

    @staticmethod
    def get_by_photographer(photographer_id):
        """Get all services for a photographer."""
        services_data = fetch_all(
            "SELECT * FROM services WHERE photographer_id = %s",
            (photographer_id,)
        )
        return [Service(s) for s in services_data]

    @staticmethod
    def get_by_category(category_id):
        """Get all services in a category."""
        services_data = fetch_all(
            "SELECT * FROM services WHERE service_category_id = %s",
            (category_id,)
        )
        return [Service(s) for s in services_data]

    @staticmethod
    def get_all():
        """Get all services."""
        services_data = fetch_all("SELECT * FROM services")
        return [Service(s) for s in services_data]

    @staticmethod
    def create(photographer_id, name, service_category_id, description=None):
        """Create a new service."""
        service_id = execute_query(
            """
            INSERT INTO services (photographer_id, name, description, service_category_id, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (photographer_id, name, description, service_category_id, datetime.utcnow())
        )
        return Service.get_by_id(service_id)

    @staticmethod
    def update(service_id, **kwargs):
        """Update service."""
        allowed_fields = ['name', 'description', 'service_category_id']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(service_id)
            query = f"UPDATE services SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return Service.get_by_id(service_id)

    @staticmethod
    def delete(service_id):
        """Delete a service."""
        execute_query("DELETE FROM services WHERE id = %s", (service_id,))

    def __repr__(self):
        return f'<Service {self.name}>'


class ServicePackage:
    """Service package model for service pricing and details."""

    def __init__(self, package_dict):
        """Initialize service package from database dictionary."""
        if package_dict:
            self.id = package_dict.get('id')
            self.service_id = package_dict.get('service_id')
            self.package_name = package_dict.get('package_name')
            self.price = package_dict.get('price')
            self.details = package_dict.get('details')
            self.location = package_dict.get('location')
            self.duration = package_dict.get('duration')
            self.created_at = package_dict.get('created_at')

    @staticmethod
    def get_by_id(package_id):
        """Get service package by ID."""
        package_data = fetch_one(
            "SELECT * FROM service_packages WHERE id = %s",
            (package_id,)
        )
        return ServicePackage(package_data) if package_data else None

    @staticmethod
    def get_by_service(service_id):
        """Get all packages for a service."""
        packages_data = fetch_all(
            "SELECT * FROM service_packages WHERE service_id = %s",
            (service_id,)
        )
        return [ServicePackage(p) for p in packages_data]

    @staticmethod
    def get_all():
        """Get all service packages."""
        packages_data = fetch_all("SELECT * FROM service_packages")
        return [ServicePackage(p) for p in packages_data]

    @staticmethod
    def create(service_id, package_name, price, details=None, location=None, duration=None):
        """Create a new service package."""
        package_id = execute_query(
            """
            INSERT INTO service_packages (service_id, package_name, price, details, location, duration, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (service_id, package_name, price, details, location, duration, datetime.utcnow())
        )
        return ServicePackage.get_by_id(package_id)

    @staticmethod
    def update(package_id, **kwargs):
        """Update service package."""
        allowed_fields = ['package_name', 'price', 'details', 'location', 'duration']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(package_id)
            query = f"UPDATE service_packages SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return ServicePackage.get_by_id(package_id)

    @staticmethod
    def delete(package_id):
        """Delete a service package."""
        execute_query("DELETE FROM service_packages WHERE id = %s", (package_id,))

    def __repr__(self):
        return f'<ServicePackage {self.package_name}>'


class Booking:
    """Booking model for customer bookings."""

    def __init__(self, booking_dict):
        """Initialize booking from database dictionary."""
        if booking_dict:
            self.id = booking_dict.get('id')
            self.customer_id = booking_dict.get('customer_id')
            self.booking_number = booking_dict.get('booking_number')
            self.service_fee = booking_dict.get('service_fee')
            self.processing_fee = booking_dict.get('processing_fee')
            self.total_price = booking_dict.get('total_price')
            self.status = booking_dict.get('status')
            self.created_at = booking_dict.get('created_at')

    @staticmethod
    def get_by_id(booking_id):
        """Get booking by ID."""
        booking_data = fetch_one(
            "SELECT * FROM bookings WHERE id = %s",
            (booking_id,)
        )
        return Booking(booking_data) if booking_data else None

    @staticmethod
    def get_by_booking_number(booking_number):
        """Get booking by booking number."""
        booking_data = fetch_one(
            "SELECT * FROM bookings WHERE booking_number = %s",
            (booking_number,)
        )
        return Booking(booking_data) if booking_data else None

    @staticmethod
    def get_by_customer(customer_id):
        """Get all bookings for a customer."""
        bookings_data = fetch_all(
            "SELECT * FROM bookings WHERE customer_id = %s ORDER BY created_at DESC",
            (customer_id,)
        )
        return [Booking(b) for b in bookings_data]

    @staticmethod
    def get_all():
        """Get all bookings."""
        bookings_data = fetch_all("SELECT * FROM bookings ORDER BY created_at DESC")
        return [Booking(b) for b in bookings_data]

    @staticmethod
    def create(customer_id, booking_number, service_fee, processing_fee, total_price, status='pending'):
        """Create a new booking."""
        booking_id = execute_query(
            """
            INSERT INTO bookings (customer_id, booking_number, service_fee, processing_fee,
                                 total_price, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (customer_id, booking_number, service_fee, processing_fee, total_price, status, datetime.utcnow())
        )
        return Booking.get_by_id(booking_id)

    @staticmethod
    def update_status(booking_id, status):
        """Update booking status."""
        execute_query(
            "UPDATE bookings SET status = %s WHERE id = %s",
            (status, booking_id)
        )
        return Booking.get_by_id(booking_id)

    @staticmethod
    def delete(booking_id):
        """Delete a booking."""
        execute_query("DELETE FROM bookings WHERE id = %s", (booking_id,))

    def __repr__(self):
        return f'<Booking {self.booking_number}>'


class BookingItem:
    """Booking item model for individual services in a booking."""

    def __init__(self, booking_item_dict):
        """Initialize booking item from database dictionary."""
        if booking_item_dict:
            self.id = booking_item_dict.get('id')
            self.booking_id = booking_item_dict.get('booking_id')
            self.service_package_id = booking_item_dict.get('service_package_id')
            self.photographer_id = booking_item_dict.get('photographer_id')
            self.service_price = booking_item_dict.get('service_price')
            self.event_start = booking_item_dict.get('event_start')
            self.event_location = booking_item_dict.get('event_location')
            self.event_notes = booking_item_dict.get('event_notes')
            self.event_pax = booking_item_dict.get('event_pax')
            self.created_at = booking_item_dict.get('created_at')

    @staticmethod
    def get_by_id(booking_item_id):
        """Get booking item by ID."""
        item_data = fetch_one(
            "SELECT * FROM booking_items WHERE id = %s",
            (booking_item_id,)
        )
        return BookingItem(item_data) if item_data else None

    @staticmethod
    def get_by_booking(booking_id):
        """Get all items for a booking."""
        items_data = fetch_all(
            "SELECT * FROM booking_items WHERE booking_id = %s",
            (booking_id,)
        )
        return [BookingItem(i) for i in items_data]

    @staticmethod
    def get_by_photographer(photographer_id):
        """Get all booking items for a photographer."""
        items_data = fetch_all(
            "SELECT * FROM booking_items WHERE photographer_id = %s ORDER BY event_start DESC",
            (photographer_id,)
        )
        return [BookingItem(i) for i in items_data]

    @staticmethod
    def create(booking_id, service_package_id, photographer_id, service_price,
               event_start, event_location=None, event_notes=None, event_pax=None):
        """Create a new booking item."""
        item_id = execute_query(
            """
            INSERT INTO booking_items (booking_id, service_package_id, photographer_id,
                                      service_price, event_start, event_location,
                                      event_notes, event_pax, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (booking_id, service_package_id, photographer_id, service_price,
             event_start, event_location, event_notes, event_pax, datetime.utcnow())
        )
        return BookingItem.get_by_id(item_id)

    @staticmethod
    def update(booking_item_id, **kwargs):
        """Update booking item."""
        allowed_fields = ['service_price', 'event_start', 'event_location', 'event_notes', 'event_pax']
        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)

        if updates:
            values.append(booking_item_id)
            query = f"UPDATE booking_items SET {', '.join(updates)} WHERE id = %s"
            execute_query(query, tuple(values))

        return BookingItem.get_by_id(booking_item_id)

    @staticmethod
    def delete(booking_item_id):
        """Delete a booking item."""
        execute_query("DELETE FROM booking_items WHERE id = %s", (booking_item_id,))

    def __repr__(self):
        return f'<BookingItem {self.id}>'


class Payment:
    """Payment model for booking payments."""

    def __init__(self, payment_dict):
        """Initialize payment from database dictionary."""
        if payment_dict:
            self.id = payment_dict.get('id')
            self.booking_id = payment_dict.get('booking_id')
            self.total_price = payment_dict.get('total_price')
            self.card_last4 = payment_dict.get('card_last4')
            self.cardholder_name = payment_dict.get('cardholder_name')
            self.card_expiry = payment_dict.get('card_expiry')
            self.status = payment_dict.get('status')
            self.payment_date = payment_dict.get('payment_date')
            self.created_at = payment_dict.get('created_at')

    @staticmethod
    def get_by_id(payment_id):
        """Get payment by ID."""
        payment_data = fetch_one(
            "SELECT * FROM payments WHERE id = %s",
            (payment_id,)
        )
        return Payment(payment_data) if payment_data else None

    @staticmethod
    def get_by_booking(booking_id):
        """Get all payments for a booking."""
        payments_data = fetch_all(
            "SELECT * FROM payments WHERE booking_id = %s ORDER BY created_at DESC",
            (booking_id,)
        )
        return [Payment(p) for p in payments_data]

    @staticmethod
    def create(booking_id, total_price, card_last4=None, cardholder_name=None,
               card_expiry=None, status='pending', payment_date=None):
        """Create a new payment."""
        payment_id = execute_query(
            """
            INSERT INTO payments (booking_id, total_price, card_last4, cardholder_name,
                                 card_expiry, status, payment_date, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (booking_id, total_price, card_last4, cardholder_name, card_expiry,
             status, payment_date, datetime.utcnow())
        )
        return Payment.get_by_id(payment_id)

    @staticmethod
    def update_status(payment_id, status, payment_date=None):
        """Update payment status."""
        if payment_date is None:
            payment_date = datetime.utcnow()
        execute_query(
            "UPDATE payments SET status = %s, payment_date = %s WHERE id = %s",
            (status, payment_date, payment_id)
        )
        return Payment.get_by_id(payment_id)

    def __repr__(self):
        return f'<Payment {self.id}>'
