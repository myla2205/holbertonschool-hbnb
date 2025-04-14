#!/usr/bin/python3

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services import facade

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=True, description='Is admin of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'message': 'User created successfully' }, 201

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Logic to update user details
        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password
            }, 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        new_amenity = facade.create_amenity(request.json)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
            }, 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.response(200, 'Amenity updated successfully')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to update an amenity
        updated_amenity = facade.update_amenity(amenity_id, request.json)
        if updated_amenity:
            return {
                'message': 'Amenity updated successfully',
                'amenity': {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name
                }
            }, 200
        else:
            return {'error': 'Amenity not found'}, 404

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Logic to update the place
        updated_place = facade.update_place(place_id, request.json)
        if not updated_place:
            return {'error': 'Place not found'}, 404
        return {'message': 'Place updated successfully'}, 200