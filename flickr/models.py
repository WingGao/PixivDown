from django.db import models


# {
#         "name": "Shadowpillar",
#         "description": "Taken with a neutral density 8 filter.\nAdded some detail extraction and reduced the saturation in Color Efex Pro\n\nThank you all for the views, comments and faves!",
#         "is_public": "1",
#         "is_friend": "0",
#         "is_family": "0",
#         "count_comments": "53",
#         "count_faves": "99+",
#         "is_video": false,
#         "sizes": {
#             "sq": {
#                 "label": "Square",
#                 "file": "14148622703_557994b6fd_s.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_s.jpg",
#                 "width": 75,
#                 "height": 75
#             },
#             "q": {
#                 "label": "Large Square",
#                 "file": "14148622703_557994b6fd_q.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_q.jpg",
#                 "width": "150",
#                 "height": "150"
#             },
#             "t": {
#                 "label": "Thumbnail",
#                 "file": "14148622703_557994b6fd_t.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_t.jpg",
#                 "width": "100",
#                 "height": "67"
#             },
#             "s": {
#                 "label": "Small",
#                 "file": "14148622703_557994b6fd_m.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_m.jpg",
#                 "width": "240",
#                 "height": "160"
#             },
#             "n": {
#                 "label": "Small 320",
#                 "file": "14148622703_557994b6fd_n.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_n.jpg",
#                 "width": "320",
#                 "height": 213
#             },
#             "m": {
#                 "label": "Medium",
#                 "file": "14148622703_557994b6fd.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd.jpg",
#                 "width": "500",
#                 "height": "333"
#             },
#             "z": {
#                 "label": "Medium 640",
#                 "file": "14148622703_557994b6fd_z.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_z.jpg",
#                 "width": "640",
#                 "height": "427"
#             },
#             "c": {
#                 "label": "Medium 800",
#                 "file": "14148622703_557994b6fd_c.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_c.jpg",
#                 "width": "800",
#                 "height": 534
#             },
#             "l": {
#                 "label": "Large",
#                 "file": "14148622703_557994b6fd_b.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_557994b6fd_b.jpg",
#                 "width": "1024",
#                 "height": "683"
#             },
#             "h": {
#                 "label": "Large 1600",
#                 "file": "14148622703_f62f6c3b43_h.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_f62f6c3b43_h.jpg",
#                 "width": "1600",
#                 "height": 1066
#             },
#             "k": {
#                 "label": "Large 2048",
#                 "file": "14148622703_ff052328a9_k.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_ff052328a9_k.jpg",
#                 "width": "2048",
#                 "height": 1365
#             },
#             "o": {
#                 "label": "Original",
#                 "file": "14148622703_feef3e6761_o.jpg",
#                 "url": "https://c2.staticflickr.com/8/7360/14148622703_feef3e6761_o.jpg",
#                 "width": "4573",
#                 "height": "3048"
#             }
#         },
#         "id": "14148622703",
#         "src": null,
#         "width": null,
#         "height": null,
#         "character_name": "Gikon",
#         "ownername": "Gikon",
#         "photo_url": "/photos/88083861@N03/14148622703/in/explore-2014-05-07",
#         "user_url": "/photos/88083861@N03",
#         "nsid": "88083861@N03",
#         "needs_interstitial": 0,
#         "show_fuzzies": false,
#         "size": "ju",
#         "full_name": "Shadowpillar",
#         "canfave": true,
#         "is_fave": false,
#         "count_comments_num": "53",
#         "spaceball": "https://s.yimg.com/pw/images/spaceball.gif",
#         "context_position": 0
#     },

class FlickrItem(models.Model):
    pid = models.BigIntegerField(unique=True, db_index=True)
    size = models.CharField(max_length=2)
    link = models.URLField()
    is_download = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def get_filename(self):
        return self.link.split('/')[-1]


