#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=============================="
echo "JWT Authentication Tests"
echo "=============================="
echo ""

# =============================
# Authentication Tests
# =============================
echo "=== Authentication Tests ==="
echo ""

# Create a user
echo "1. Creating user..."
USER1=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Alice","last_name":"Smith","email":"alice@test.com","password":"password123"}')
USER1_ID=$(echo "$USER1" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo "   User created: $USER1_ID"

# Login with correct credentials
echo "2. Login with correct credentials..."
LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"password123"}')
TOKEN1=$(echo "$LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
if [ -n "$TOKEN1" ]; then
    echo "   ✅ Login successful"
else
    echo "   ❌ Login failed"
fi

# Login with wrong password
echo "3. Login with wrong password..."
WRONG_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@test.com","password":"wrongpassword"}')
ERROR=$(echo "$WRONG_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', ''))")
if [ "$ERROR" = "Invalid credentials" ]; then
    echo "   ✅ Login correctly rejected"
else
    echo "   ❌ Login should have been rejected"
fi

echo ""
# =============================
# Places Endpoint Tests
# =============================
echo "=== Places Endpoint Tests ==="
echo ""

# Create place without token (should fail)
echo "1. Creating place without token (should fail)..."
NO_TOKEN_PLACE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test House","price":100,"latitude":40.7,"longitude":-74.0,"amenities":[]}')
ERROR=$(echo "$NO_TOKEN_PLACE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', ''))")
if [ "$ERROR" = "Authentication token is missing" ]; then
    echo "   ✅ Place creation correctly rejected without token"
else
    echo "   ❌ Place creation should have been rejected"
fi

# Create place with token (should succeed)
echo "2. Creating place with token (should succeed)..."
PLACE1=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d '{"title":"Alice House","price":100,"latitude":40.7,"longitude":-74.0,"amenities":[]}')
PLACE1_ID=$(echo "$PLACE1" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
if [ -n "$PLACE1_ID" ]; then
    echo "   ✅ Place created successfully: $PLACE1_ID"
else
    echo "   ❌ Place creation failed"
fi

# Get places without token (should succeed - public)
echo "3. Getting all places without token (should succeed)..."
PUBLIC_PLACES=$(curl -s -w "%{http_code}" -o /dev/null $BASE_URL/places/)
if [ "$PUBLIC_PLACES" = "200" ]; then
    echo "   ✅ Public access to places works"
else
    echo "   ❌ Public access failed with code: $PUBLIC_PLACES"
fi

# Create second user to test ownership
echo "4. Creating second user..."
USER2=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Bob","last_name":"Jones","email":"bob@test.com","password":"password123"}')
USER2_ID=$(echo "$USER2" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

LOGIN2=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"bob@test.com","password":"password123"}')
TOKEN2=$(echo "$LOGIN2" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
echo "   User2 created: $USER2_ID"

# User2 tries to update User1's place (should fail)
echo "5. User2 trying to update User1's place (should fail)..."
UPDATE_FAIL=$(curl -s -X PUT $BASE_URL/places/$PLACE1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d '{"title":"Hacked House","price":1,"latitude":40.7,"longitude":-74.0,"amenities":[]}')
ERROR=$(echo "$UPDATE_FAIL" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', ''))")
if [[ "$ERROR" == *"permission"* ]]; then
    echo "   ✅ Update correctly rejected"
else
    echo "   ❌ Update should have been rejected"
fi

# User1 updates their own place (should succeed)
echo "6. User1 updating their own place (should succeed)..."
UPDATE_SUCCESS=$(curl -s -X PUT $BASE_URL/places/$PLACE1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d '{"title":"Updated House","price":150,"latitude":40.7,"longitude":-74.0,"amenities":[]}')
MESSAGE=$(echo "$UPDATE_SUCCESS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('message', ''))")
if [[ "$MESSAGE" == *"successfully"* ]]; then
    echo "   ✅ Place updated successfully"
else
    echo "   ❌ Place update failed"
fi

echo ""
# =============================
# Reviews Endpoint Tests
# =============================
echo "=== Reviews Endpoint Tests ==="
echo ""

# User1 tries to review their own place (should fail)
echo "1. User1 trying to review their own place (should fail)..."
SELF_REVIEW=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d "{\"text\":\"Great place!\",\"place_id\":\"$PLACE1_ID\"}")
ERROR=$(echo "$SELF_REVIEW" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', ''))")
if [[ "$ERROR" == *"own place"* ]]; then
    echo "   ✅ Self-review correctly rejected"
else
    echo "   ❌ Self-review should have been rejected"
fi

# User2 reviews User1's place (should succeed)
echo "2. User2 reviewing User1's place (should succeed)..."
REVIEW1=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d "{\"text\":\"Amazing place!\",\"place_id\":\"$PLACE1_ID\"}")
REVIEW1_ID=$(echo "$REVIEW1" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
if [ -n "$REVIEW1_ID" ]; then
    echo "   ✅ Review created successfully: $REVIEW1_ID"
else
    echo "   ❌ Review creation failed"
fi

# User2 tries to review the same place again (should fail)
echo "3. User2 trying to review the same place again (should fail)..."
DUPLICATE_REVIEW=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d "{\"text\":\"Another review\",\"place_id\":\"$PLACE1_ID\"}")
ERROR=$(echo "$DUPLICATE_REVIEW" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', ''))")
if [[ "$ERROR" == *"already reviewed"* ]]; then
    echo "   ✅ Duplicate review correctly rejected"
else
    echo "   ❌ Duplicate review should have been rejected"
fi

# User2 updates their review (should succeed)
echo "4. User2 updating their review (should succeed)..."
UPDATE_REVIEW=$(curl -s -X PUT $BASE_URL/reviews/$REVIEW1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d '{"text":"Updated: Even better!"}')
TEXT=$(echo "$UPDATE_REVIEW" | python3 -c "import sys, json; print(json.load(sys.stdin).get('text', ''))")
if [[ "$TEXT" == *"Updated"* ]]; then
    echo "   ✅ Review updated successfully"
else
    echo "   ❌ Review update failed"
fi

# User1 tries to update User2's review (should fail)
echo "5. User1 trying to update User2's review (should fail)..."
WRONG_UPDATE=$(curl -s -X PUT $BASE_URL/reviews/$REVIEW1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d '{"text":"Hacked review!"}')
ERROR=$(echo "$WRONG_UPDATE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', ''))")
if [[ "$ERROR" == *"permission"* ]]; then
    echo "   ✅ Update correctly rejected"
else
    echo "   ❌ Update should have been rejected"
fi

# User1 tries to delete User2's review (should fail)
echo "6. User1 trying to delete User2's review (should fail)..."
WRONG_DELETE=$(curl -s -w "%{http_code}" -o /tmp/delete_output.txt -X DELETE $BASE_URL/reviews/$REVIEW1_ID \
  -H "Authorization: Bearer $TOKEN1")
if [ "$WRONG_DELETE" = "403" ]; then
    echo "   ✅ Delete correctly rejected"
else
    echo "   ❌ Delete should have been rejected with 403, got: $WRONG_DELETE"
fi

# User2 deletes their own review (should succeed)
echo "7. User2 deleting their own review (should succeed)..."
DELETE_SUCCESS=$(curl -s -w "%{http_code}" -o /dev/null -X DELETE $BASE_URL/reviews/$REVIEW1_ID \
  -H "Authorization: Bearer $TOKEN2")
if [ "$DELETE_SUCCESS" = "204" ]; then
    echo "   ✅ Review deleted successfully"
else
    echo "   ❌ Review delete failed with code: $DELETE_SUCCESS"
fi

# Get reviews without token (should succeed - public)
echo "8. Getting all reviews without token (should succeed)..."
PUBLIC_REVIEWS=$(curl -s -w "%{http_code}" -o /dev/null $BASE_URL/reviews/)
if [ "$PUBLIC_REVIEWS" = "200" ]; then
    echo "   ✅ Public access to reviews works"
else
    echo "   ❌ Public access failed with code: $PUBLIC_REVIEWS"
fi

echo ""
# =============================
# Users Endpoint Tests
# =============================
echo "=== Users Endpoint Tests ==="
echo ""

# User1 updates their own profile (should succeed)
echo "1. User1 updating their own profile (should succeed)..."
UPDATE_PROFILE=$(curl -s -X PUT $BASE_URL/users/$USER1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d '{"first_name":"AliceUpdated","last_name":"SmithUpdated","email":"alice@test.com","password":"password123"}')
FNAME=$(echo "$UPDATE_PROFILE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('first_name', ''))")
if [ "$FNAME" = "AliceUpdated" ]; then
    echo "   ✅ Profile updated successfully"
else
    echo "   ❌ Profile update failed"
fi

# User1 tries to update User2's profile (should fail)
echo "2. User1 trying to update User2's profile (should fail)..."
WRONG_PROFILE=$(curl -s -w "%{http_code}" -o /tmp/profile_output.txt -X PUT $BASE_URL/users/$USER2_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN1" \
  -d '{"first_name":"Hacked","last_name":"User","email":"bob@test.com","password":"password123"}')
if [ "$WRONG_PROFILE" = "403" ]; then
    echo "   ✅ Profile update correctly rejected"
else
    echo "   ❌ Profile update should have been rejected with 403, got: $WRONG_PROFILE"
fi

# Get users without token (should succeed - public)
echo "3. Getting all users without token (should succeed)..."
PUBLIC_USERS=$(curl -s -w "%{http_code}" -o /dev/null $BASE_URL/users/)
if [ "$PUBLIC_USERS" = "200" ]; then
    echo "   ✅ Public access to users works"
else
    echo "   ❌ Public access failed with code: $PUBLIC_USERS"
fi

echo ""
echo "=============================="
echo "All Tests Completed"
echo "=============================="
