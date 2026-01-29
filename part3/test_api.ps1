$BaseUrl = "http://127.0.0.1:5000/api/v1"
$Passed = 0
$Failed = 0

function Assert-Status { param($Name, $Expected, $Actual)
    if ($Actual -eq $Expected) {
        Write-Host "  OK $Name : $Actual" -ForegroundColor Green
        $script:Passed++
    } else {
        Write-Host "  FAIL $Name : expected $Expected, got $Actual" -ForegroundColor Red
        $script:Failed++
    }
}

Write-Host "`n=== HBnB Part3 API Tests ===" -ForegroundColor Cyan

try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing
    Assert-Status "GET /" 200 $r.StatusCode
} catch { Assert-Status "GET /" 200 $_.Exception.Response.StatusCode.value__ }

try {
    $login = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method POST -ContentType "application/json" -Body '{"email":"admin@example.com","password":"admin123"}'
    $token = $login.access_token
    if ($token) { Write-Host "  OK Login: token received" -ForegroundColor Green; $script:Passed++ }
    else { Write-Host "  FAIL Login: no token" -ForegroundColor Red; $script:Failed++ }
} catch {
    Write-Host "  FAIL Login: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Start server: python run.py" -ForegroundColor Gray
    exit 1
}

$headers = @{ "Authorization" = "Bearer $token"; "Content-Type" = "application/json" }

try {
    $user = Invoke-RestMethod -Uri "$BaseUrl/users/" -Method POST -Headers $headers -Body '{"first_name":"Test","last_name":"User","email":"testuser@example.com","password":"pass123"}'
    $userId = $user.id
    Write-Host "  OK POST /users/ : created" -ForegroundColor Green
    $script:Passed++
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 400 -and $_.ErrorDetails.Message -match "already exists") {
        $users = Invoke-RestMethod -Uri "$BaseUrl/users/" -Method GET -Headers $headers
        $userId = ($users | Where-Object { $_.email -eq "testuser@example.com" } | Select-Object -First 1).id
        Write-Host "  OK POST /users/ : email exists (rerun)" -ForegroundColor Gray
    } else {
        Write-Host "  FAIL POST /users/: $($_.Exception.Message)" -ForegroundColor Red
        $script:Failed++
    }
}

try {
    $r = Invoke-WebRequest -Uri "$BaseUrl/users/" -Method GET -Headers $headers -UseBasicParsing
    Assert-Status "GET /users/ (admin)" 200 $r.StatusCode
} catch { Assert-Status "GET /users/" 200 $_.Exception.Response.StatusCode.value__ }

if ($userId) {
    try {
        $r = Invoke-WebRequest -Uri "$BaseUrl/users/$userId" -Method GET -Headers $headers -UseBasicParsing
        Assert-Status "GET /users/<id>" 200 $r.StatusCode
    } catch { Assert-Status "GET /users/<id>" 200 $_.Exception.Response.StatusCode.value__ }
}

try {
    $amenity = Invoke-RestMethod -Uri "$BaseUrl/amenities/" -Method POST -Headers $headers -Body '{"name":"WiFi"}'
    $amenityId = $amenity.id
    Write-Host "  OK POST /amenities/ : created" -ForegroundColor Green
    $script:Passed++
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 400) {
        $amenities = Invoke-RestMethod -Uri "$BaseUrl/amenities/" -Method GET
        $amenityId = ($amenities | Where-Object { $_.name -eq "WiFi" } | Select-Object -First 1).id
        Write-Host "  OK POST /amenities/ : exists (rerun)" -ForegroundColor Gray
    } else {
        Write-Host "  FAIL POST /amenities/: $($_.Exception.Message)" -ForegroundColor Red
        $script:Failed++
    }
}

try {
    $r = Invoke-WebRequest -Uri "$BaseUrl/amenities/" -Method GET -UseBasicParsing
    Assert-Status "GET /amenities/ (public)" 200 $r.StatusCode
} catch { Assert-Status "GET /amenities/" 200 $_.Exception.Response.StatusCode.value__ }

try {
    $userLogin = Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method POST -ContentType "application/json" -Body '{"email":"testuser@example.com","password":"pass123"}'
    $userHeaders = @{ "Authorization" = "Bearer $($userLogin.access_token)"; "Content-Type" = "application/json" }
    try {
        Invoke-RestMethod -Uri "$BaseUrl/users/" -Method POST -Headers $userHeaders -Body '{"first_name":"X","last_name":"Y","email":"x@x.com","password":"p"}' | Out-Null
        Write-Host "  FAIL RBAC: non-admin should be blocked" -ForegroundColor Red
        $script:Failed++
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -eq 403) {
            Write-Host "  OK RBAC: non-admin blocked (403)" -ForegroundColor Green
            $script:Passed++
        } else {
            Write-Host "  FAIL RBAC: expected 403, got $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
            $script:Failed++
        }
    }
} catch {
    Write-Host "  SKIP RBAC test (test user may not exist)" -ForegroundColor Gray
}

Write-Host "`n=== $Passed passed, $Failed failed ===" -ForegroundColor Cyan
if ($Failed -gt 0) { exit 1 }
