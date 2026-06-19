import json
import os

from agents.ats_agent import ATSAgent


class ATSService:

    def __init__(self):
        self.agent = ATSAgent()

    def analyze_all(self):
        # Load JD
        with open("uploads/jd/jd.json", "r") as f:
            jd_data = json.load(f)

        candidates = []
        resume_dir = "uploads/resumes"

        # Process all resumes
        for file in os.listdir(resume_dir):
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(resume_dir, file)

            with open(file_path, "r") as f:
                resume_data = json.load(f)

            result = self.agent.evaluate_candidate(jd_data, resume_data)

            # Generate Candidate ID
            result["candidate_id"] = len(candidates) + 1
            result["resume_file"] = file
            candidates.append(result)

        # Sort by ATS Score
        candidates.sort(key=lambda x: x["ats_score"], reverse=True)

        # Assign Rank
        for index, candidate in enumerate(candidates):
            candidate["rank"] = index + 1

        # Create Rankings Folder
        os.makedirs("uploads/rankings", exist_ok=True)

        # Save Ranking JSON
        with open("uploads/rankings/ranking.json", "w") as f:
            json.dump(candidates, f, indent=4)

        return {
            "status": "success",
            "total_candidates": len(candidates),
            "rankings": candidates
        }

    def rank_candidates(self, jd_data, resumes):
        candidates = []

        for resume_data in resumes:
            result = self.agent.evaluate_candidate(jd_data, resume_data)
            result["candidate_id"] = len(candidates) + 1
            candidates.append(result)

        # Sort by ATS Score
        candidates.sort(key=lambda x: x["ats_score"], reverse=True)

        # Assign Rank
        for index, candidate in enumerate(candidates):
            candidate["rank"] = index + 1

        return candidates