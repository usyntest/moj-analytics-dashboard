import requests
from datetime import datetime
import concurrent.futures

headers = {
    'user-agent': 'Moj/24.16.1 (in.mohalla.video; build:20240626164318; iOS 17.5.1) Alamofire/5.9.0',
    'x-sharechat-userid': '59276572841',
    'x-sharechat-secret': '81dec8fc79eae6fc525d',
    'country-short': 'IN',
    'accept': '*/*',
    'content-type': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
}

class Dashboard:
    def __init__(self, search_string):
        self.search_string = search_string
        self.dashboard_data = {
            "total_posts": 0,
            "total_interactions": 0,
            "latest_posts": [],
            "tags": [],
            "categories": {},
            "languages": {},
            "accounts": [],
        }

        self.graph_colors = [
            '#007BA7',  # Cerulean Blue
            '#F4C430',  # Saffron
            '#E34234',  # Vermilion
            '#4CBB17',  # Kelly Green
            '#9C51B6',  # Purple Plum
            '#DAA520',  # Goldenrod
            '#40E0D0',  # Turquoise
            '#FF7F50',  # Coral
            '#6A5ACD',  # Slate Blue
            '#DC143C'   # Crimson
        ]

    def get_dataset_from_moj(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for offset in range(1000 // 8):
                executor.submit(self.process_page, offset)

    def process_page(self, offset):
        response = requests.get("https://moj-apis.sharechat.com/search-service/v1.0.0/all-search", params={
            "lang": "English",
            "postOffset": offset * 8,
            "searchString": self.search_string,
            "variant": "variant-1"
        }, headers=headers)

        for post in response.json().get("postData", {}).get("postCards", []):
            self.create_dashboard_data(self.create_post_dict(post)) 


    def create_dashboard_data(self, post):

        # Total no. of posts
        self.dashboard_data["total_posts"] += 1 
        
        # Category distribution over data
        category_name = post.get("user_data", {}).get("genre", None)
        if category_name:
            self.dashboard_data["categories"][category_name] = self.dashboard_data["categories"].get(category_name, 0) + 1


        # Language distribution in data
        language_name = post.get("user_data", {}).get("language", None)
        if language_name:
            self.dashboard_data["languages"][language_name] = self.dashboard_data["languages"].get(language_name, 0) + 1

        # Total interactions
        likes =  0 if post["post_data"]["likes"] is None else int(post["post_data"]["likes"])
        comments = 0 if post["post_data"]["comments"] is None else int(post["post_data"]["comments"])
        interactions = likes + comments
        self.dashboard_data["total_interactions"] += int(interactions)

        # Tag distribution over data
        for tag in post["post_data"].get("tag_list", []):
            tag_id = tag["tag_id"]

            tag_found = False
            for existing_tag in self.dashboard_data["tags"]:
                if existing_tag.get("tag_id") == tag_id:
                    existing_tag["posts"] += 1
                    existing_tag["interactions"] += interactions
                    tag_found = True
                    break
            
            if not tag_found:
                self.dashboard_data["tags"].append({
                    "tag_id": tag_id,
                    "posts": 1,
                    "interactions": interactions,
                    "tag_name": tag.get("tag_name", None),
                    "tag_hash": tag.get("tag_hash", None)
                })

        
        user_id = post["user_data"]["user_id"]
        if user_id:
            user_found = False
            for user in self.dashboard_data["accounts"]:
                if user.get("user_id") == user_id:
                    user["posts"] += 1
                    user["interactions"] = user["interactions"] + int(interactions)
                    user_found = True
                    break
            
            if not user_found:
                self.dashboard_data["accounts"].append({
                    "user_id": user_id,
                    "username": post.get("user_data", {}).get("username", None),
                    "posts": 1,
                    "interactions": int(interactions),
                    "name": post.get("user_data", {}).get("user_name", None),
                    "profile_img": post.get("user_data", {}).get("user_profile_image", None)
                })

        self.dashboard_data["latest_posts"].append(post)

    def get_latest_posts(self, top_n=10):
        # Sort posts by date in descending order
        sorted_posts = sorted(self.dashboard_data["latest_posts"], key=lambda x: x["post_data"]["time"], reverse=True)
        return sorted_posts[:top_n]


    def get_top_accounts_by_interactions(self, top_n=10):
        sorted_accounts = sorted(self.dashboard_data["accounts"], key=lambda x: x["interactions"], reverse=True)
        return sorted_accounts[:top_n]
    

    def get_top_tags_by_interactions(self, top_n=10):
        sorted_tags = sorted(self.dashboard_data["tags"], key=lambda x: x["interactions"], reverse=True)
        return sorted_tags[:top_n]
    

    @staticmethod
    def get_highest_bandwidth_video_url(bandwidth_parsed_videos):
        if bandwidth_parsed_videos is None or len(bandwidth_parsed_videos) <= 0:
            return None
        
        highest_bitrate = 0
        url = ""
        for video in bandwidth_parsed_videos:
            if video["bitrate"] > highest_bitrate:
                url = video["url"]

        return url[:url.find("?")]


    @staticmethod
    def extract_user_data(user_block):
        if not user_block:
            return None
        return {
            "user_name": user_block.get("n", None),
            "username": user_block.get("h", None),
            "user_id": user_block.get("i", None),
            "user_profile_image": user_block.get("pu", None),
            "user_age": user_block.get("authorAge", None),
            "user_like_count": user_block.get("likeCount", None),
            "creator_type": user_block.get("creatorGradeDetails", {}).get("creatorType", None),
            "genre": user_block.get("creatorGradeDetails", {}).get("genre", None),
            "language": user_block.get("creatorGradeDetails", {}).get("lang", None),
            "tenant": user_block.get("creatorGradeDetails", {}).get("tenant", None),
            "object_type": user_block.get("creatorGradeDetails", {}).get("objectType", None),
            "status": user_block.get("s", None)
        }


    @staticmethod
    def extract_post_data(post_block):
        if not post_block:
            return None
        return {
            "content_type": post_block.get("t", None),
            "time": datetime.fromtimestamp(int(post_block.get("o", None), 0)),
            "type": post_block.get("st", None),
            "genres": post_block.get("taxonomy", None),
            "likes": post_block.get("lc", None),
            "comments": post_block.get("c2", None),
            "news_publisher_status": post_block.get("newsPublisherStatus", None),
            "attributed_video_url": post_block.get("attributedVideoUrl", None),
            "video_link": Dashboard.get_highest_bandwidth_video_url(post_block.get("bandwidthParsedVideos", None)),
            "perma_link": post_block.get("permalink", None),
            "caption": post_block.get("c", None),
            "thumbnail": post_block.get("thumb", None),
            "tag_list": [{
                "tag_hash": tag.get("tagHash", None),
                "tag_id": tag.get("tagId", None),
                "tag_name": tag.get("tagName", None)
            } for tag in post_block["captionTagsList"]] if post_block.get("captionTagsList", []) else [],
        }


    @staticmethod
    def create_post_dict(post):
        return {
            "user_data": Dashboard.extract_user_data(post.get('ath', None)),
            "post_data": Dashboard.extract_post_data(post)
        }
