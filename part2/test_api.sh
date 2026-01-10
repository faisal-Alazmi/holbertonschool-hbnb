#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=============================="
echo "Running HBnB API Tests"
echo "=============================="
echo ""

# -----------------------------
# USERS
# -----------------------------
echo "Testing Users endpoints..."

# 1. Create valid user
echo -n "POST /users/ (valid user): "
USER_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/user.json -X POST $BASE_URL/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"1234"}')
USER_STATUS=${USER_RESPONSE:(-3)}
if [ "$USER_STATUS" == "201" ]; then echo "✅ $USER_STATUS"; else echo "❌ $USER_STATUS"; fi
USER_ID=$(jq -r '.id' /tmp/user.json)

# 2. Create invalid user (missing email)
echo -n "POST /users/ (missing email): "
USER_INVALID=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"Jane","last_name":"Doe","password":"1234"}')
if [ "$USER_INVALID" == "400" ]; then echo "✅ $USER_INVALID"; else echo "❌ $USER_INVALID"; fi

# 3. Get all users
echo -n "GET /users/: "
ALL_USERS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/users/)
if [ "$ALL_USERS" == "200" ]; then echo "✅ $ALL_USERS"; else echo "❌ $ALL_USERS"; fi

# 4. Get single user
echo -n "GET /users/<id>: "
SINGLE_USER=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/users/$USER_ID)
if [ "$SINGLE_USER" == "200" ]; then echo "✅ $SINGLE_USER"; else echo "❌ $SINGLE_USER"; fi

echo ""
# -----------------------------
# PLACES
# -----------------------------
echo "Testing Places endpoints..."

# 1. Create valid place (FIXED: uses correct fields)
echo -n "POST /places/ (valid): "
PLACE_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/place.json -X POST $BASE_URL/places/ \
-H "Content-Type: application/json" \
-d "{\"title\":\"Cozy Cottage\",\"description\":\"A nice place\",\"price\":100.0,\"latitude\":40.7128,\"longitude\":-74.0060,\"owner_id\":\"$USER_ID\",\"amenities\":[]}")
PLACE_STATUS=${PLACE_RESPONSE:(-3)}
if [ "$PLACE_STATUS" == "201" ]; then 
    echo "✅ $PLACE_STATUS"
    PLACE_ID=$(jq -r '.id' /tmp/place.json)
else 
    echo "❌ $PLACE_STATUS"
    cat /tmp/place.json
    PLACE_ID=""
fi

# 2. Invalid owner
echo -n "POST /places/ (invalid owner): "
PLACE_INVALID=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/places/ \
-H "Content-Type: application/json" \
-d '{"title":"Mansion","description":"Big house","price":500.0,"latitude":40.7128,"longitude":-74.0060,"owner_id":"fake-id","amenities":[]}')
if [ "$PLACE_INVALID" == "400" ]; then echo "✅ $PLACE_INVALID"; else echo "❌ $PLACE_INVALID"; fi

# 3. Get all places
echo -n "GET /places/: "
ALL_PLACES=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/places/)
if [ "$ALL_PLACES" == "200" ]; then echo "✅ $ALL_PLACES"; else echo "❌ $ALL_PLACES"; fi

# 4. Get single place (FIXED: only test if PLACE_ID exists)
if [ -n "$PLACE_ID" ]; then
    echo -n "GET /places/<id>: "
    SINGLE_PLACE=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/places/$PLACE_ID)
    if [ "$SINGLE_PLACE" == "200" ]; then echo "✅ $SINGLE_PLACE"; else echo "❌ $SINGLE_PLACE"; fi
else
    echo "GET /places/<id>: ⏭️  SKIPPED (no place created)"
fi

echo ""
# -----------------------------
# REVIEWS
# -----------------------------
echo "Testing Reviews endpoints..."

# Only test reviews if we have a valid place
if [ -n "$PLACE_ID" ]; then
    # 1. Create valid review
    echo -n "POST /reviews/ (valid): "
    REVIEW_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/review.json -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"Great place!\",\"user_id\":\"$USER_ID\",\"place_id\":\"$PLACE_ID\"}")
    REVIEW_STATUS=${REVIEW_RESPONSE:(-3)}
    if [ "$REVIEW_STATUS" == "201" ]; then 
        echo "✅ $REVIEW_STATUS"
        REVIEW_ID=$(jq -r '.id' /tmp/review.json)
    else 
        echo "❌ $REVIEW_STATUS"
        cat /tmp/review.json
        REVIEW_ID=""
    fi

    # 2. Missing user_id
    echo -n "POST /reviews/ (missing user_id): "
    REVIEW_INVALID=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"Nice\",\"place_id\":\"$PLACE_ID\"}")
    if [ "$REVIEW_INVALID" == "400" ]; then echo "✅ $REVIEW_INVALID"; else echo "❌ $REVIEW_INVALID"; fi

    # 3. Get all reviews
    echo -n "GET /reviews/: "
    ALL_REVIEWS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/reviews/)
    if [ "$ALL_REVIEWS" == "200" ]; then echo "✅ $ALL_REVIEWS"; else echo "❌ $ALL_REVIEWS"; fi

    # 4. Get single review
    if [ -n "$REVIEW_ID" ]; then
        echo -n "GET /reviews/<id>: "
        SINGLE_REVIEW=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/reviews/$REVIEW_ID)
        if [ "$SINGLE_REVIEW" == "200" ]; then echo "✅ $SINGLE_REVIEW"; else echo "❌ $SINGLE_REVIEW"; fi
    else
        echo "GET /reviews/<id>: ⏭️  SKIPPED (no review created)"
    fi
else
    echo "Reviews tests: ⏭️  SKIPPED (no place available)"
fi

echo ""
# -----------------------------
# AMENITIES
# -----------------------------
echo "Testing Amenities endpoints..."

# 1. Create valid amenity
echo -n "POST /amenities/ (valid): "
AMENITY_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/amenity.json -X POST $BASE_URL/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}')
AMENITY_STATUS=${AMENITY_RESPONSE:(-3)}
if [ "$AMENITY_STATUS" == "201" ]; then echo "✅ $AMENITY_STATUS"; else echo "❌ $AMENITY_STATUS"; fi
AMENITY_ID=$(jq -r '.id' /tmp/amenity.json)

# 2. Missing name
echo -n "POST /amenities/ (missing name): "
AMENITY_INVALID=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/amenities/ \
-H "Content-Type: application/json" \
-d '{}')
if [ "$AMENITY_INVALID" == "400" ]; then echo "✅ $AMENITY_INVALID"; else echo "❌ $AMENITY_INVALID"; fi

# 3. Get all amenities
echo -n "GET /amenities/: "
ALL_AMENITIES=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/amenities/)
if [ "$ALL_AMENITIES" == "200" ]; then echo "✅ $ALL_AMENITIES"; else echo "❌ $ALL_AMENITIES"; fi

# 4. Get single amenity
echo -n "GET /amenities/<id>: "
SINGLE_AMENITY=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/amenities/$AMENITY_ID)
if [ "$SINGLE_AMENITY" == "200" ]; then echo "✅ $SINGLE_AMENITY"; else echo "❌ $SINGLE_AMENITY"; fi

echo ""
echo "=============================="
echo "HBnB API Tests Completed"
echo "=============================="
