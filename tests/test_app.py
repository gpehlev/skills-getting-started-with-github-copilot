from src import app as app_module


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == app_module.activities


def test_signup_for_activity(client):
    email = "new.student@mergington.edu"
    activity_name = "Art Studio"
    starting_participants = list(app_module.activities[activity_name]["participants"])

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert app_module.activities[activity_name]["participants"] == starting_participants + [email]
    assert app_module.activities["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_rejects_duplicate_registration(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_activity_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Robotics Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity(client):
    activity_name = "Science Club"
    email = "mia@mergington.edu"
    starting_participants = list(app_module.activities[activity_name]["participants"])

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert app_module.activities[activity_name]["participants"] == [participant for participant in starting_participants if participant != email]


def test_unregister_from_activity_returns_404_when_not_signed_up(client):
    response = client.delete("/activities/Science Club/signup", params={"email": "missing@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_from_activity_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Robotics Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}