from flask import escape, Flask, request, jsonify, json
import functions_framework


# import firebase
from firebase_admin import firestore, credentials, initialize_app

# Application Default credentials are automatically created.
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

# tables
voters = db.collection("voters")
elections = db.collection("elections")


@app.route("/register_voter", methods=["POST"])
def register_voter(request):
    # Making sure data is passed as a request
    if not request.data:
        return jsonify({"Error": "No data has been passed :("}), 400
    user_id = request.json["user_id"]

    # check if user is already registered
    stu_exists = voters.document(user_id).get().exists
    if stu_exists:
        return jsonify({"error": "already exists"}), 404

    voters.document(user_id).set(request.json)
    return jsonify(request.json), 201


@app.route("/register_election", methods=["POST"])
def register_election(request):
    record = json.loads(request.data)
    record["voters"] = []

    # Making sure data is passed as a request
    if not request.data:
        return jsonify({"Error": "No data has been passed :("}), 400
    election_id = request.json["election_id"]

    # check if election is already registered
    election_exists = elections.document(election_id).get().exists
    if election_exists:
        return (
            jsonify(
                {
                    "error": f"{record['election_name']} Elections with ID {record['election_id']}, already exists"
                }
            ),
            404,
        )

    elections.document(election_id).set(request.json)
    return jsonify(request.json), 201


@app.route("/deregister_voter", methods=["DELETE"])
def deregister_voter(request):
    user_id = request.args.get("user_id")

    # check if user is already registered
    stu_exists = voters.document(user_id).get().exists

    if not stu_exists:
        return jsonify({"Message": "User does not exist"}), 404

    user = voters.document(user_id).get()
    user.reference.delete()
    return jsonify(
        {"Message": f"Voter with id {user_id} has been deleted successfully"}
    )


@app.route("/delete_election", methods=["DELETE"])
def delete_election(request):
    election_id = request.args.get("election_id")

    # check if election is already registered
    election_exists = elections.document(election_id).get().exists

    if not election_exists:
        return (
            jsonify({"Message": f"This election does not exist in the database"}),
            404,
        )

    election = elections.document(election_id).get()

    election.reference.delete()
    return jsonify(
        {"Message": f"The election id {election_id} has been deleted successfully"}
    )


@app.route("/get_voter", methods=["GET"])
def get_voter(request):
    user_id = request.args.get("user_id")
    voter_ref = db.collection("voters").document(user_id)
    voter_doc = voter_ref.get()

    if not voter_doc.exists:
        return jsonify({"Message": "Voter does not exist"}), 404

    voter_data = voter_doc.to_dict()
    return jsonify(voter_data)


@app.route("/get_election", methods=["GET"])
def get_election(request):
    election_id = request.args.get("election_id")
    election_ref = db.collection("elections").document(election_id)
    election_doc = election_ref.get()

    if not election_doc.exists:
        return jsonify({"Message": "Election does not exist"}), 404

    election_data = election_doc.to_dict()

    return jsonify(election_data)


@app.route("/update_voter", methods=["PUT"])
def update_voter(request):
    user_id = request.args.get("user_id")
    record = json.loads(request.data)
    # check if user exists
    voter_ref = db.collection("voters").document(user_id)
    voter_doc = voter_ref.get()

    if not voter_doc.exists:
        return jsonify({"Message": "Voter does not exist"}), 404

    # update the voter details
    update_dict = {}
    if "major" in record:
        update_dict["major"] = record["major"]
    if "first_name" in record:
        update_dict["first_name"] = record["first_name"]
    if "last_name" in record:
        update_dict["last_name"] = record["last_name"]
    if "year" in record:
        update_dict["year"] = record["year"]

    voter_ref.update(update_dict)

    # retrieve and return the updated voter data
    voter_doc = db.collection("voters").document(user_id).get()
    voter_data = voter_doc.to_dict()
    return jsonify(voter_data)


@app.route("/elections/vote", methods=["POST"])
def vote_in_election(request):
    voter_id = request.args.get("voter_id")
    election_id = request.args.get("election_id")
    candidate_id = request.args.get("candidate_id")

    # check if voter been registered
    voter_ref = db.collection("voters").where("user_id", "==", voter_id).get()

    if not voter_ref:
        return (
            jsonify({"error": "You are not registered to vote in this election :("}),
            404,
        )

    # check if election exists
    elections_ref = (
        db.collection("elections").where("election_id", "==", election_id).get()
    )
    if not elections_ref:
        return jsonify({"error": "Election not found."}), 404

        # check if voter has already voted in this election
    election_ref = db.collection("elections").document(election_id)
    if election_ref.get().exists:
        election_data = election_ref.get().to_dict()
        voters_list = election_data.get("voters")
        if voters_list:
            if voter_id in voters_list:
                return (
                    jsonify({"error": "You have already voted in this election."}),
                    400,
                )

        # check if candidate exists in this election
    candidates = election_data.get("candidates")
    updated_candidates = list()
    candidate_exists = False
    for candidate in candidates:
        if candidate["user_id"] == candidate_id:
            candidate["vote_count"] += 1
            candidate_exists = True

            # add the voter to the list of voters
            election_ref.update({"voters": firestore.ArrayUnion([voter_id])})
        updated_candidates.append(candidate)

    # updating the candidates in the election collection
    election_ref.update({"candidates": updated_candidates})

    if not candidate_exists:
        return (
            jsonify({"error": "This candidate is not standing in this election."}),
            404,
        )

    return jsonify({"success": "Your vote has been counted."}), 201
