I want to create a web app called ZSchool.  

here is a brief for a display layer over a the top of a Canvas LMS API to allow my daughter to better access her work

we need to start by getting  the latest message that outlines the work required for the week - check if new course content.  This should be polled daily and update the content based on the 
curl "https://learning.acc.edu.au/api/v1/announcements?context_codes[]=course_20564&latest_only=true" \
  -H "Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D"


Take the payload and use an LLM to parse it to get only content related to lessons.  I want you to extract the class work into json format


  example payload:
[{"id":242182,"title":"Week starting Monday 28 July","last_reply_at":"2025-07-27T22:30:12Z","created_at":"2025-07-25T04:32:13Z","delayed_post_at":"2025-07-27T22:30:00Z","posted_at":"2025-07-27T22:30:12Z","assignment_id":null,"root_topic_id":null,"position":26,"podcast_has_student_posts":false,"discussion_type":"threaded","lock_at":null,"allow_rating":true,"only_graders_can_rate":false,"sort_by_rating":false,"is_section_specific":false,"anonymous_state":null,"summary_enabled":false,"user_name":"Norm Fitzgerald","discussion_subentry_count":0,"permissions":{"attach":false,"update":false,"reply":true,"delete":false,"manage_assign_to":false},"require_initial_post":null,"user_can_see_posts":true,"podcast_url":null,"read_state":"read","unread_count":0,"subscribed":false,"attachments":[],"published":true,"can_unpublish":false,"locked":false,"can_lock":true,"comments_disabled":false,"author":{"id":11791,"anonymous_id":"93j","display_name":"Norm Fitzgerald","avatar_image_url":"https://learning.acc.edu.au/images/thumbnails/10478276/ZBtNVJK2P1xMGrkHsedO7CtqNQlSQIU0Lryb7zYN","html_url":"https://learning.acc.edu.au/courses/20564/users/11791","pronouns":null},"html_url":"https://learning.acc.edu.au/courses/20564/discussion_topics/242182","url":"https://learning.acc.edu.au/courses/20564/discussion_topics/242182","pinned":false,"group_category_id":null,"can_group":false,"topic_children":[],"group_topic_children":[],"context_code":"course_20564","ungraded_discussion_overrides":null,"locked_for_user":false,"message":"\u003clink rel=\"stylesheet\" href=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/9694035/Updated%20Mobile%20CSS%20file21%253A11.css\"\u003e\u003clink rel=\"stylesheet\" href=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/1236185/canvas_global_app.css\"\u003e\u003cp\u003e\u003ciframe class=\"lti-embed\" style=\"width: 720px; height: 405px; display: inline-block;\" title=\"IMG_4667\" src=\"https://learning.acc.edu.au/courses/20564/external_tools/retrieve?display=borderless\u0026amp;url=https%3A%2F%2Faccde.instructuremedia.com%2Flti%2Flaunch%3Fcustom_arc_launch_type%3Dbare_embed%26custom_arc_media_id%3D1c242615-3fdd-4240-9bb9-0c1b9b149247-212400%26custom_arc_start_at%3D0\" width=\"720\" height=\"405\" allowfullscreen=\"allowfullscreen\" webkitallowfullscreen=\"webkitallowfullscreen\" mozallowfullscreen=\"mozallowfullscreen\" allow=\"geolocation *; microphone *; camera *; midi *; encrypted-media *; autoplay *; clipboard-write *; display-capture *\" data-studio-resizable=\"true\" data-studio-tray-enabled=\"true\" data-studio-convertible-to-link=\"true\" loading=\"lazy\"\u003e\u003c/iframe\u003e\u003c/p\u003e\n\u003cp\u003eWelcome to Term 3 students! I hope you had a restful Winter Holiday and are ready for an exciting time of learning.\u003c/p\u003e\n\u003cp\u003eA particularly warm welcome to our new student joining us this term. I hope your time in DE is rewarding and we thank you for joining us.\u003c/p\u003e\n\u003cp\u003eHere is your work for this week.\u003c/p\u003e\n\u003cp\u003e\u003cspan style=\"text-decoration: underline;\"\u003e\u003cstrong\u003eThis Week's Work (starting Monday 28 July)\u003c/strong\u003e\u003c/span\u003e\u003c/p\u003e\n\u003col\u003e\n\u003cli aria-level=\"1\"\u003e\u003cstrong\u003eSpiritual and Physical Fitness:\u003c/strong\u003e\u003cspan\u003e Unit 3 Week 3 Physical Fitness and Lessons 11-15.\u003c/span\u003e\u003c/li\u003e\n\u003cli\u003e\u003cstrong\u003eMaths:\u003c/strong\u003e\u003cspan\u003e Topic 9: All lesson pages listed as B1 to B5.\u003c/span\u003e\u003c/li\u003e\n\u003cli aria-level=\"1\"\u003e\u003cstrong\u003eEnglish:\u0026nbsp;\u003c/strong\u003eUnit 11, Lessons 1-5.\u0026nbsp;\u003cspan\u003e(\u003c/span\u003e\u003cem\u003ePlease submit your Informative, Imaginative and Persuasive Sentences)\u003c/em\u003e\u003c/li\u003e\n\u003cli\u003e\u003cstrong\u003eTechnology (Mon, Tue, Thur, Fri):\u003c/strong\u003e\u003cspan\u003e Unit 3 Lessons 1-4.\u0026nbsp;\u003c/span\u003e\u003cspan\u003e(\u003c/span\u003e\u003cem\u003ePlease submit your Binary Image assessment. Your Digital Design Project will be due on Sunday, 17 August, not the end of the term as mentioned in your lessons)\u003c/em\u003e\u003c/li\u003e\n\u003cli\u003e\u003cspan\u003e\u003cstrong\u003eHPE (Wed):\u003c/strong\u003e Health: Unit 3 Lesson 3; PE: Unit 3 Lesson 3.\u003c/span\u003e\u003c/li\u003e\n\u003c/ol\u003e\n\u003cp\u003eThe Term Index is no longer available. For further information on assessment due date, go to your \u003cstrong\u003eCanvas Calendar\u003c/strong\u003e or refer to your \u003cstrong\u003eTo Do List\u003c/strong\u003e.\u003c/p\u003e\n\u003cp\u003eTicking off \u003cstrong\u003e'Mark as Done'\u003c/strong\u003e after each lesson will help you keep track of your progress.\u003c/p\u003e\n\u003cp\u003e\u003cspan style=\"text-decoration: underline;\"\u003e\u003cstrong\u003eUploading Assessments and Accessing Quizzes\u003c/strong\u003e\u003c/span\u003e\u003c/p\u003e\n\u003cul\u003e\n\u003cli\u003eDue Dates for assessments and quizzes are now on the \u003cstrong\u003eSunday after\u003c/strong\u003e they appear in the lesson.\u003c/li\u003e\n\u003cli\u003eYou can upload assessments and access quizzes for a period of at least \u003cstrong\u003eone week before and after\u003c/strong\u003e the assessment or quiz appears in a lesson. You will be unable to do the assessment if it is locked outside of this timeframe.\u003c/li\u003e\n\u003cli\u003eIf you are sick, travelling or competing in an elite sport, use the \u003cstrong\u003eflexibility\u003c/strong\u003e of this two week window to keep up with your lessons, assessments and quizzes.\u003c/li\u003e\n\u003cli\u003eIf you are sick or injured and \u003cstrong\u003ecannot complete an assessment\u003c/strong\u003e, follow the Attendance procedure in Communication Hub to be excused. Submit your \u003cstrong\u003eDoctor's Certificate\u003c/strong\u003e as proof with this form.\u003c/li\u003e\n\u003cli\u003e\u003cstrong\u003eDo not email\u003c/strong\u003e assessments to teachers.\u003c/li\u003e\n\u003cli\u003eWe ask students and Supervisors to be aware of this timeframe and \u003cstrong\u003eplan your work schedule\u003c/strong\u003e accordingly. Do not ask for assessments or quizzes to be opened up early, or made available later, than these times.\u003c/li\u003e\n\u003c/ul\u003e\n\u003cp\u003e\u003cspan style=\"text-decoration: underline;\"\u003e\u003cstrong\u003eClass Connect\u003c/strong\u003e\u003c/span\u003e\u003c/p\u003e\n\u003cp\u003eClass Connect starts next \u003cstrong\u003eMonday at 9.00\u003c/strong\u003e.\u003c/p\u003e\n\u003cp\u003eIf you are a new student, welcome to Distance Education! Class Connect is our way of connecting as a Year 5/6 class. You get a chance to meet me as your teacher and some of your other DE class mates. We get to hear each other's opinions on hot topics, play games like Kahoot and Blooket, and get secret tips on how to succeed at school. All students are welcome!\u003c/p\u003e\n\u003cp\u003e\u003cspan style=\"text-decoration: underline;\"\u003e\u003cstrong\u003eAre you a New DE Student/Supervisor?\u003c/strong\u003e\u003c/span\u003e\u003c/p\u003e\n\u003cp\u003eI will be holding an Induction Google Meet this \u003cstrong\u003eWednesday, 30 July at 9am \u003c/strong\u003efor new students and supervisors.\u003c/p\u003e\n\u003cp\u003eUse \u003ca class=\"inline_disabled\" href=\"https://meet.google.com/ids-iwku-fud\" target=\"_blank\"\u003e\u003cstrong\u003ethis link\u003c/strong\u003e\u003c/a\u003e to attend the meeting on the Supervisor's device.\u003c/p\u003e\n\u003cp\u003eIt would be great if the student was on their device ready to go on their Dashboard in Canvas so you can both follow along and attend the meeting at the same time.\u003c/p\u003e\n\u003cp\u003eHave an spectacular week students!\u003c/p\u003e\n\u003cp\u003eNorm Fitzgerald,\u003c/p\u003e\n\u003cp\u003eStage 3 Teacher.\u003c/p\u003e\u003cscript src=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/9694034/Updated%20mobile%2021%253A11js.js\"\u003e\u003c/script\u003e\u003cscript src=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/1341919/BlueCanvasMobileConfig.js\"\u003e\u003c/script\u003e","subscription_hold":"topic_is_announcement","todo_date":null,"is_announcement":true,"sort_order":"asc","sort_order_locked":false,"expanded":true,"expanded_locked":false}]



I want the json format returned to always match 

{
  "week_starting": "2025-07-28",
  "title": "Week starting Monday 28 July",
  "teacher": {
    "name": "Norm Fitzgerald",
    "role": "Stage 3 Teacher"
  },
  "classwork": [
    {
      "subject": "Spiritual and Physical Fitness",
      "unit": "Unit 3",
      "topic": "",
      "lessons": ["11", "12", "13", "14", "15"],
      "days": [],
      "notes": []
    },
    {
      "subject": "Maths",
      "unit": "",
      "topic": "Topic 9",
      "lessons": ["B1", "B2", "B3", "B4", "B5"],
      "days": [],
      "notes": []
    },
    {
      "subject": "English",
      "unit": "Unit 11",
      "topic": "",
      "lessons": ["1", "2", "3", "4", "5"],
      "days": [],
      "notes": [
        "Please submit your Informative, Imaginative and Persuasive Sentences"
      ]
    },
    {
      "subject": "Technology",
      "unit": "Unit 3",
      "topic": "",
      "lessons": ["1", "2", "3", "4"],
      "days": ["Monday", "Tuesday", "Thursday", "Friday"],
      "notes": [
        "Please submit your Binary Image assessment",
        "Digital Design Project due on Sunday, 17 August (not end of term as mentioned in lessons)"
      ]
    },
    {
      "subject": "Health",
      "unit": "Unit 3",
      "topic": "",
      "lessons": ["3"],
      "days": ["Wednesday"],
      "notes": []
    },
    {
      "subject": "PE",
      "unit": "Unit 3",
      "topic": "",
      "lessons": ["3"],
      "days": ["Wednesday"],
      "notes": []
    }
  ],
  "announcements": [
    {
      "type": "term_start",
      "message": "Welcome to Term 3"
    },
    {
      "type": "new_student",
      "message": "Welcome to our new student joining us this term"
    },
    {
      "type": "term_index_notice",
      "message": "The Term Index is no longer available. Use the Canvas Calendar or To Do List."
    },
    {
      "type": "mark_as_done_tip",
      "message": "Use 'Mark as Done' to keep track of lesson completion"
    }
  ],
  "assessment_and_quizzes": {
    "due_day": "Sunday",
    "access_window": "1 week before and after lesson appears",
    "exceptions": [
      "If sick, travelling or in elite sport, use the 2-week window",
      "If unable to complete, use the Attendance form in the Communication Hub and submit a Doctor's Certificate"
    ],
    "guidelines": [
      "Do not email assessments to teachers",
      "Plan ahead; no early or late access will be granted"
    ]
  },
  "class_connect": {
    "start_time": "Monday at 9:00",
    "description": "Live class session to meet your teacher and classmates, play games, and get school tips"
  },
  "induction_meeting": {
    "audience": "New DE students and supervisors",
    "datetime": "2025-07-30T09:00:00+10:00",
    "link": "https://meet.google.com/ids-iwku-fud",
    "instructions": "Student should be on their device and logged into Canvas Dashboard"
  }
}

I want to add the content from announcements and assessments_and_quizes as page alert content on the final page





Call to get all the courses
curl "https://learning.acc.edu.au/api/v1/courses?access_token=13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D"


from the payload extract all ID's eg  "id": 22859 and name eg. "name": "2025 Primary Orientation Course (MPDE)" for each of the subjects

  example payload:

  [
  {
    "id": 21734,
    "name": "2025 Communication Hub (MPDE)",
    "account_id": 68,
    "uuid": "qdZbM18G8aCYPRXHcFudetk30SdRczcVGlTHxpD4",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-25T01:51:58Z",
    "course_code": "2025 Communication Hub (MPDE)",
    "default_view": "wiki",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_qdZbM18G8aCYPRXHcFudetk30SdRczcVGlTHxpD4.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 22859,
    "name": "2025 Primary Orientation Course (MPDE)",
    "account_id": 68,
    "uuid": "rDsdtYWSDTszEFyYWWL1qUF3vKshwfrMifu2BhEX",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-12-24T01:40:49Z",
    "course_code": "2025 Primary Orientation Course (MPDE)",
    "default_view": "wiki",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_rDsdtYWSDTszEFyYWWL1qUF3vKshwfrMifu2BhEX.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": false,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20520,
    "name": "2025 Year 6 Arts (MPDE)",
    "account_id": 348,
    "uuid": "yhu9NlK6mUjo0p5KfKsdJhF9mswpAqHgkEQKZfol",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-13T06:27:53Z",
    "course_code": "2025 Year 6 Arts (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_yhu9NlK6mUjo0p5KfKsdJhF9mswpAqHgkEQKZfol.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20428,
    "name": "2025 Year 6 English (MPDE)",
    "account_id": 348,
    "uuid": "7Sxz9NYsneZ35xTpeNA4M9M8RYuvQo8od5HlNAaF",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-13T04:00:13Z",
    "course_code": "2025 Year 6 English (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_7Sxz9NYsneZ35xTpeNA4M9M8RYuvQo8od5HlNAaF.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20429,
    "name": "2025 Year 6 English Literature (MPDE)",
    "account_id": 348,
    "uuid": "OnAW3xFX0pdrQbIelYKKl0sHc4HnQ04Pn9HZoKkE",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-13T04:00:24Z",
    "course_code": "2025 Year 6 English Literature (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_OnAW3xFX0pdrQbIelYKKl0sHc4HnQ04Pn9HZoKkE.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20498,
    "name": "2025 Year 6 HASS (MPDE)",
    "account_id": 348,
    "uuid": "5fyoxKaWwbNZn5bNv9shD40JGqb3GWbj0RC3UMjf",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-13T06:27:50Z",
    "course_code": "2025 Year 6 HASS (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_5fyoxKaWwbNZn5bNv9shD40JGqb3GWbj0RC3UMjf.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20430,
    "name": "2025 Year 6 HPE (MPDE)",
    "account_id": 348,
    "uuid": "NagSD6FFvfmzhxlyclgCUnPm29Htq8l05bG27jve",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-13T04:00:32Z",
    "course_code": "2025 Year 6 HPE (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_NagSD6FFvfmzhxlyclgCUnPm29Htq8l05bG27jve.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20354,
    "name": "2025 Year 6 Maths (MPDE)",
    "account_id": 348,
    "uuid": "l4blbuj69XY76hWxfYyRg1NFM5mCWQwec5PHPyOF",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-11T22:30:54Z",
    "course_code": "2025 Year 6 Maths (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_l4blbuj69XY76hWxfYyRg1NFM5mCWQwec5PHPyOF.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20476,
    "name": "2025 Year 6 Science (MPDE)",
    "account_id": 348,
    "uuid": "rALxEbPado0PKvzAyS56BA2taoA9O3h1tulJCCUY",
    "start_at": null,
    "grading_standard_id": null,
    "is_public": false,
    "created_at": "2024-11-13T06:15:54Z",
    "course_code": "2025 Year 6 Science (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_rALxEbPado0PKvzAyS56BA2taoA9O3h1tulJCCUY.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  },
  {
    "id": 20564,
    "name": "2025 Year 6 Spiritual & Physical Fitness (MPDE)",
    "account_id": 348,
    "uuid": "ptsa2zKjINfLPfWW6QUOmDWIRTIYQVZ2LZzdctrT",
    "start_at": null,
    "grading_standard_id": 84,
    "is_public": false,
    "created_at": "2024-11-13T06:27:58Z",
    "course_code": "2025 Year 6 Spiritual & Physical Fitness (MPDE)",
    "default_view": "modules",
    "root_account_id": 1,
    "enrollment_term_id": 152,
    "license": "private",
    "grade_passback_setting": null,
    "end_at": null,
    "public_syllabus": false,
    "public_syllabus_to_auth": false,
    "storage_quota_mb": 10485,
    "is_public_to_auth_users": false,
    "homeroom_course": false,
    "course_color": null,
    "friendly_name": null,
    "apply_assignment_group_weights": false,
    "calendar": {
      "ics": "https://learning.acc.edu.au/feeds/calendars/course_ptsa2zKjINfLPfWW6QUOmDWIRTIYQVZ2LZzdctrT.ics"
    },
    "time_zone": "Australia/Sydney",
    "blueprint": false,
    "template": false,
    "enrollments": [
      {
        "type": "student",
        "role": "StudentEnrollment",
        "role_id": 3,
        "user_id": 54197,
        "enrollment_state": "active",
        "limit_privileges_to_course_section": false
      }
    ],
    "hide_final_grades": true,
    "workflow_state": "available",
    "restrict_enrollments_to_course_dates": false
  }
]



for each of the courses above (by ID) Get all modules for a course (subject)
curl "https://learning.acc.edu.au/api/v1/courses/{{course ID}}/modules?per_page=50" \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'

for exmple

curl "https://learning.acc.edu.au/api/v1/courses/20354/modules?per_page=50" \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'


here is an example payload (We will need to search each course (by course ID) to find the modules that we need based on the UNIT or TOPIC from the first API call in the 'name' field).  These will be partial matches... for example in the payload below according to the original API calls return value for math (which has course ID 20354) we are looking for Topic 9 which would correspond to "name": "Year 6 Maths - Topic 9 - Area and Perimeter"

We will need to get all of the IDs for these matches along with 'name' as it appears in the payload


[
  {
    "id": 297929,
    "name": "Resource Lists",
    "position": 2,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "completed",
    "completed_at": "2025-07-25T03:33:35Z",
    "items_count": 1,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/297929/items"
  },
  {
    "id": 286715,
    "name": "Y6 - MATHS - 2025 Information",
    "position": 3,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "completed",
    "completed_at": "2025-07-25T07:58:14Z",
    "items_count": 3,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/286715/items"
  },
  {
    "id": 253384,
    "name": "Year 6 Maths - Topic 1 - Numbers and Number Patterns",
    "position": 4,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "started",
    "completed_at": null,
    "items_count": 17,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253384/items"
  },
  {
    "id": 253385,
    "name": "Year 6 Maths - Topic 2 - Mixed Operations",
    "position": 5,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "started",
    "completed_at": null,
    "items_count": 22,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253385/items"
  },
  {
    "id": 253386,
    "name": "Year 6 Maths - Topic 3 - Angles",
    "position": 6,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "started",
    "completed_at": null,
    "items_count": 9,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253386/items"
  },
  {
    "id": 253387,
    "name": "Year 6 Maths - Topic 4 - Transformations",
    "position": 7,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "started",
    "completed_at": null,
    "items_count": 14,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253387/items"
  },
  {
    "id": 253388,
    "name": "Year 6 Maths - Topic 5 - Fractions",
    "position": 8,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 32,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253388/items"
  },
  {
    "id": 253389,
    "name": "Year 6 Maths - Topic 6 - Time",
    "position": 9,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 7,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253389/items"
  },
  {
    "id": 253390,
    "name": "Year 6 Maths - Topic 7 - Addition and Subtraction of Decimals",
    "position": 10,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 13,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253390/items"
  },
  {
    "id": 253391,
    "name": "Year 6 Maths - Topic 8 - Multiplication and Division of Decimals",
    "position": 11,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 20,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253391/items"
  },
  {
    "id": 253392,
    "name": "Year 6 Maths - Topic 9 - Area and Perimeter",
    "position": 13,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "started",
    "completed_at": null,
    "items_count": 10,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253392/items"
  },
  {
    "id": 253393,
    "name": "Year 6 Maths - Topic 10 - Areas of Triangles and Parallelograms",
    "position": 14,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 9,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253393/items"
  },
  {
    "id": 253394,
    "name": "Year 6 Maths - Topic 11 - 3D Objects",
    "position": 15,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 6,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253394/items"
  },
  {
    "id": 253395,
    "name": "Year 6 Maths - Topic 12 - Cartesian Plane",
    "position": 16,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 6,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253395/items"
  },
  {
    "id": 253396,
    "name": "Year 6 Maths - Topic 13 - Volume and Capacity",
    "position": 18,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 10,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253396/items"
  },
  {
    "id": 253399,
    "name": "Year 6 Maths - Topic 14 - Percentage",
    "position": 20,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 20,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253399/items"
  },
  {
    "id": 253400,
    "name": "Year 6 Maths - Topic 15 - Data",
    "position": 21,
    "unlock_at": null,
    "require_sequential_progress": false,
    "requirement_type": "all",
    "publish_final_grade": false,
    "prerequisite_module_ids": [],
    "state": "unlocked",
    "completed_at": null,
    "items_count": 14,
    "items_url": "https://learning.acc.edu.au/api/v1/courses/20354/modules/253400/items"
  }
]


get the ID of the modules we need, along with name and items_url


use this ID to extract the Topics for the module. we will use the ID above to do this.  The call for this has the structure

curl "https://learning.acc.edu.au/api/v1/courses/{{course ID}}/modules/{{module ID}}/items?per_page=50"  \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'


for example

curl "https://learning.acc.edu.au/api/v1/courses/20354/modules/253389/items?per_page=50"  \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'


The returned Payload will look like this

[
  {
    "id": 2567723,
    "title": "Topic 6 - Let's Remember",
    "position": 1,
    "indent": 0,
    "quiz_lti": false,
    "type": "Page",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2567723",
    "page_url": "topic-6-lets-remember",
    "publish_at": null,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-lets-remember",
    "completion_requirement": {
      "type": "must_mark_done",
      "completed": false
    }
  },
  {
    "id": 2253020,
    "title": "Topic 6 - Unit 1 - Lesson 1 - Finding Duration of Time",
    "position": 3,
    "indent": 1,
    "quiz_lti": false,
    "type": "Page",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2253020",
    "page_url": "topic-6-unit-1-lesson-1-finding-duration-of-time",
    "publish_at": null,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-unit-1-lesson-1-finding-duration-of-time",
    "completion_requirement": {
      "type": "must_mark_done",
      "completed": false
    }
  },
  {
    "id": 2253021,
    "title": "Topic 6 - Unit 1 - Lesson 2 - Finding End Time",
    "position": 4,
    "indent": 1,
    "quiz_lti": false,
    "type": "Page",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2253021",
    "page_url": "topic-6-unit-1-lesson-2-finding-end-time",
    "publish_at": null,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-unit-1-lesson-2-finding-end-time",
    "completion_requirement": {
      "type": "must_mark_done",
      "completed": false
    }
  },
  {
    "id": 2253022,
    "title": "Topic 6 - Unit 1 - Lesson 3 - Finding Start Time",
    "position": 5,
    "indent": 1,
    "quiz_lti": false,
    "type": "Page",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2253022",
    "page_url": "topic-6-unit-1-lesson-3-finding-start-time",
    "publish_at": null,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-unit-1-lesson-3-finding-start-time",
    "completion_requirement": {
      "type": "must_mark_done",
      "completed": false
    }
  },
  {
    "id": 2253024,
    "title": "Topic 6 - Unit 2 - Lesson 1 - Reading and Interpreting Timetables",
    "position": 7,
    "indent": 1,
    "quiz_lti": false,
    "type": "Page",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2253024",
    "page_url": "topic-6-unit-2-lesson-1-reading-and-interpreting-timetables",
    "publish_at": null,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-unit-2-lesson-1-reading-and-interpreting-timetables",
    "completion_requirement": {
      "type": "must_mark_done",
      "completed": false
    }
  },
  {
    "id": 2253025,
    "title": "Topic 6 - Unit 2 - Lesson 2 - Using Timetables",
    "position": 8,
    "indent": 1,
    "quiz_lti": false,
    "type": "Page",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2253025",
    "page_url": "topic-6-unit-2-lesson-2-using-timetables",
    "publish_at": null,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-unit-2-lesson-2-using-timetables",
    "completion_requirement": {
      "type": "must_mark_done",
      "completed": false
    }
  },
  {
    "id": 2764002,
    "title": "Y6 Topic 6 - Time - Assessment",
    "position": 16,
    "indent": 3,
    "quiz_lti": false,
    "type": "Assignment",
    "module_id": 253389,
    "html_url": "https://learning.acc.edu.au/courses/20354/modules/items/2764002",
    "content_id": 1417068,
    "url": "https://learning.acc.edu.au/api/v1/courses/20354/assignments/1417068"
  }
]

We will use the lessons list from the original Payload "lessons" to find and filter the lesson items we want to find details for.

the deatils we will want to extract are the ID, Title, page_url, html_url, url, and completion_requirement->completed (boolean)


For each course I need to extract the weekly assignments.  the API for this needs to be called for all course ID's.  The API call for this looks like


curl "https://learning.acc.edu.au/api/v1/calendar_events?start_date={{Start date}}&end_date={{end date}}&type=assignment&context_codes[]=course_{{course ID}}&per_page=50" \
  -H "Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D"

  The start date needs to be the date starting monday of the current week we are in and end date needs to be the Sunday of the current week we are in.


For example:

curl "https://learning.acc.edu.au/api/v1/calendar_events?start_date=2025-07-28&end_date=2025-08-03&type=assignment&context_codes[]=course_20354&per_page=50" \
  -H "Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D"


all of the returned assignments should be put into homework.

the payload example for this is:

[
  {
    "title": "Y6 - T9 - U3 - L1",
    "description": "",
    "submission_types": "online_quiz",
    "workflow_state": "published",
    "created_at": "2024-11-20T19:42:16Z",
    "updated_at": "2025-07-21T23:47:10Z",
    "all_day": true,
    "all_day_date": "2025-08-03",
    "id": "assignment_1134635",
    "type": "assignment",
    "assignment": {
      "id": 1134635,
      "description": "",
      "due_at": "2025-08-03T13:59:59Z",
      "unlock_at": "2025-07-19T14:00:00Z",
      "lock_at": "2025-08-10T13:59:59Z",
      "points_possible": 4,
      "grading_type": "points",
      "assignment_group_id": 171921,
      "grading_standard_id": null,
      "created_at": "2024-11-20T19:42:16Z",
      "updated_at": "2025-07-21T23:47:10Z",
      "peer_reviews": false,
      "automatic_peer_reviews": false,
      "position": 5,
      "grade_group_students_individually": false,
      "anonymous_peer_reviews": false,
      "group_category_id": null,
      "post_to_sis": false,
      "moderated_grading": false,
      "omit_from_final_grade": false,
      "intra_group_peer_reviews": false,
      "anonymous_instructor_annotations": false,
      "anonymous_grading": false,
      "graders_anonymous_to_graders": false,
      "grader_count": 0,
      "grader_comments_visible_to_graders": true,
      "final_grader_id": null,
      "grader_names_visible_to_final_grader": true,
      "allowed_attempts": -1,
      "annotatable_attachment_id": null,
      "hide_in_gradebook": false,
      "suppress_assignment": false,
      "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6IjFiMDYwNWQ2LWVmZjEtNDg4OC05NWEyLTYxNTMyYjNlMzc2OCJ9.WyL4v4YMyr1uEOnmt49sSwQPt5HKFAq8K_x72cmBfic",
      "lti_context_id": "1b0605d6-eff1-4888-95a2-61532b3e3768",
      "course_id": 20354,
      "name": "Y6 - T9 - U3 - L1",
      "submission_types": [
        "online_quiz"
      ],
      "has_submitted_submissions": true,
      "due_date_required": false,
      "max_name_length": 255,
      "in_closed_grading_period": false,
      "graded_submissions_exist": true,
      "user_submitted": false,
      "is_quiz_assignment": true,
      "can_duplicate": false,
      "original_course_id": null,
      "original_assignment_id": null,
      "original_lti_resource_link_id": null,
      "original_assignment_name": null,
      "original_quiz_id": null,
      "workflow_state": "published",
      "important_dates": false,
      "muted": true,
      "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134635",
      "quiz_id": 798296,
      "anonymous_submissions": false,
      "published": true,
      "only_visible_to_overrides": false,
      "visible_to_everyone": true,
      "locked_for_user": false,
      "submissions_download_url": "https://learning.acc.edu.au/courses/20354/quizzes/798296/submissions?zip=1",
      "post_manually": false,
      "anonymize_students": false,
      "require_lockdown_browser": false,
      "restrict_quantitative_data": false
    },
    "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134635",
    "context_code": "course_20354",
    "context_name": "2025 Year 6 Maths (MPDE)",
    "context_color": null,
    "end_at": "2025-08-03T13:59:59Z",
    "start_at": "2025-08-03T13:59:59Z",
    "url": "https://learning.acc.edu.au/api/v1/calendar_events/assignment_1134635",
    "assignment_overrides": [
      {
        "id": 152879,
        "assignment_id": 1134635,
        "title": "06HR.DE",
        "due_at": "2025-08-03T13:59:59Z",
        "all_day": true,
        "all_day_date": "2025-08-03",
        "unlock_at": "2025-07-19T14:00:00Z",
        "lock_at": "2025-08-10T13:59:59Z",
        "quiz_id": 798296,
        "unassign_item": false,
        "course_section_id": 31629
      }
    ],
    "important_dates": false
  },
  {
    "title": "Y6 - T9 - U2 - L1",
    "description": "",
    "submission_types": "online_quiz",
    "workflow_state": "published",
    "created_at": "2024-11-20T19:42:21Z",
    "updated_at": "2025-07-21T23:47:05Z",
    "all_day": true,
    "all_day_date": "2025-08-03",
    "id": "assignment_1134684",
    "type": "assignment",
    "assignment": {
      "id": 1134684,
      "description": "",
      "due_at": "2025-08-03T13:59:59Z",
      "unlock_at": "2025-07-19T14:00:00Z",
      "lock_at": "2025-08-10T13:59:59Z",
      "points_possible": 4,
      "grading_type": "points",
      "assignment_group_id": 171921,
      "grading_standard_id": null,
      "created_at": "2024-11-20T19:42:21Z",
      "updated_at": "2025-07-21T23:47:05Z",
      "peer_reviews": false,
      "automatic_peer_reviews": false,
      "position": 3,
      "grade_group_students_individually": false,
      "anonymous_peer_reviews": false,
      "group_category_id": null,
      "post_to_sis": false,
      "moderated_grading": false,
      "omit_from_final_grade": false,
      "intra_group_peer_reviews": false,
      "anonymous_instructor_annotations": false,
      "anonymous_grading": false,
      "graders_anonymous_to_graders": false,
      "grader_count": 0,
      "grader_comments_visible_to_graders": true,
      "final_grader_id": null,
      "grader_names_visible_to_final_grader": true,
      "allowed_attempts": -1,
      "annotatable_attachment_id": null,
      "hide_in_gradebook": false,
      "suppress_assignment": false,
      "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6ImJkM2QxYmQ3LTg0YzgtNDUwZC1iNTg1LWM4NTM0MjBmYWQxZSJ9.DWYj9PHG4W6_cB4TuDtVwoLh3zhkoFh60vX5Q5L0pro",
      "lti_context_id": "bd3d1bd7-84c8-450d-b585-c853420fad1e",
      "course_id": 20354,
      "name": "Y6 - T9 - U2 - L1",
      "submission_types": [
        "online_quiz"
      ],
      "has_submitted_submissions": true,
      "due_date_required": false,
      "max_name_length": 255,
      "in_closed_grading_period": false,
      "graded_submissions_exist": true,
      "user_submitted": true,
      "is_quiz_assignment": true,
      "can_duplicate": false,
      "original_course_id": null,
      "original_assignment_id": null,
      "original_lti_resource_link_id": null,
      "original_assignment_name": null,
      "original_quiz_id": null,
      "workflow_state": "published",
      "important_dates": false,
      "muted": true,
      "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134684",
      "quiz_id": 798345,
      "anonymous_submissions": false,
      "published": true,
      "only_visible_to_overrides": false,
      "visible_to_everyone": true,
      "locked_for_user": false,
      "submissions_download_url": "https://learning.acc.edu.au/courses/20354/quizzes/798345/submissions?zip=1",
      "post_manually": false,
      "anonymize_students": false,
      "require_lockdown_browser": false,
      "restrict_quantitative_data": false
    },
    "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134684",
    "context_code": "course_20354",
    "context_name": "2025 Year 6 Maths (MPDE)",
    "context_color": null,
    "end_at": "2025-08-03T13:59:59Z",
    "start_at": "2025-08-03T13:59:59Z",
    "url": "https://learning.acc.edu.au/api/v1/calendar_events/assignment_1134684",
    "assignment_overrides": [
      {
        "id": 152877,
        "assignment_id": 1134684,
        "title": "06HR.DE",
        "due_at": "2025-08-03T13:59:59Z",
        "all_day": true,
        "all_day_date": "2025-08-03",
        "unlock_at": "2025-07-19T14:00:00Z",
        "lock_at": "2025-08-10T13:59:59Z",
        "quiz_id": 798345,
        "unassign_item": false,
        "course_section_id": 31629
      }
    ],
    "important_dates": false
  },
  {
    "title": "Y6 - T9 - U1 - L2",
    "description": "",
    "submission_types": "online_quiz",
    "workflow_state": "published",
    "created_at": "2024-11-20T19:42:23Z",
    "updated_at": "2025-07-21T23:47:02Z",
    "all_day": true,
    "all_day_date": "2025-08-03",
    "id": "assignment_1134708",
    "type": "assignment",
    "assignment": {
      "id": 1134708,
      "description": "",
      "due_at": "2025-08-03T13:59:59Z",
      "unlock_at": "2025-07-19T14:00:00Z",
      "lock_at": "2025-08-10T13:59:59Z",
      "points_possible": 4,
      "grading_type": "points",
      "assignment_group_id": 171921,
      "grading_standard_id": null,
      "created_at": "2024-11-20T19:42:23Z",
      "updated_at": "2025-07-21T23:47:02Z",
      "peer_reviews": false,
      "automatic_peer_reviews": false,
      "position": 2,
      "grade_group_students_individually": false,
      "anonymous_peer_reviews": false,
      "group_category_id": null,
      "post_to_sis": false,
      "moderated_grading": false,
      "omit_from_final_grade": false,
      "intra_group_peer_reviews": false,
      "anonymous_instructor_annotations": false,
      "anonymous_grading": false,
      "graders_anonymous_to_graders": false,
      "grader_count": 0,
      "grader_comments_visible_to_graders": true,
      "final_grader_id": null,
      "grader_names_visible_to_final_grader": true,
      "allowed_attempts": -1,
      "annotatable_attachment_id": null,
      "hide_in_gradebook": false,
      "suppress_assignment": false,
      "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6IjJiZWQyMmIxLTBmMDMtNGJhZS05ZmEwLWZlNmNkYjgwZjZkMSJ9._mc2EIGHl1xHRc5qzu3v7KMnoeRC65Ak-h3YQOd4k0E",
      "lti_context_id": "2bed22b1-0f03-4bae-9fa0-fe6cdb80f6d1",
      "course_id": 20354,
      "name": "Y6 - T9 - U1 - L2",
      "submission_types": [
        "online_quiz"
      ],
      "has_submitted_submissions": true,
      "due_date_required": false,
      "max_name_length": 255,
      "in_closed_grading_period": false,
      "graded_submissions_exist": true,
      "user_submitted": true,
      "is_quiz_assignment": true,
      "can_duplicate": false,
      "original_course_id": null,
      "original_assignment_id": null,
      "original_lti_resource_link_id": null,
      "original_assignment_name": null,
      "original_quiz_id": null,
      "workflow_state": "published",
      "important_dates": false,
      "muted": true,
      "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134708",
      "quiz_id": 798369,
      "anonymous_submissions": false,
      "published": true,
      "only_visible_to_overrides": false,
      "visible_to_everyone": true,
      "locked_for_user": false,
      "submissions_download_url": "https://learning.acc.edu.au/courses/20354/quizzes/798369/submissions?zip=1",
      "post_manually": false,
      "anonymize_students": false,
      "require_lockdown_browser": false,
      "restrict_quantitative_data": false
    },
    "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134708",
    "context_code": "course_20354",
    "context_name": "2025 Year 6 Maths (MPDE)",
    "context_color": null,
    "end_at": "2025-08-03T13:59:59Z",
    "start_at": "2025-08-03T13:59:59Z",
    "url": "https://learning.acc.edu.au/api/v1/calendar_events/assignment_1134708",
    "assignment_overrides": [
      {
        "id": 152876,
        "assignment_id": 1134708,
        "title": "06HR.DE",
        "due_at": "2025-08-03T13:59:59Z",
        "all_day": true,
        "all_day_date": "2025-08-03",
        "unlock_at": "2025-07-19T14:00:00Z",
        "lock_at": "2025-08-10T13:59:59Z",
        "quiz_id": 798369,
        "unassign_item": false,
        "course_section_id": 31629
      }
    ],
    "important_dates": false
  },
  {
    "title": "Y6 - T9 - U2 - L2",
    "description": "",
    "submission_types": "online_quiz",
    "workflow_state": "published",
    "created_at": "2024-11-20T19:42:42Z",
    "updated_at": "2025-07-21T23:47:07Z",
    "all_day": true,
    "all_day_date": "2025-08-03",
    "id": "assignment_1134944",
    "type": "assignment",
    "assignment": {
      "id": 1134944,
      "description": "",
      "due_at": "2025-08-03T13:59:59Z",
      "unlock_at": "2025-07-19T14:00:00Z",
      "lock_at": "2025-08-10T13:59:59Z",
      "points_possible": 4,
      "grading_type": "points",
      "assignment_group_id": 171921,
      "grading_standard_id": null,
      "created_at": "2024-11-20T19:42:42Z",
      "updated_at": "2025-07-21T23:47:07Z",
      "peer_reviews": false,
      "automatic_peer_reviews": false,
      "position": 4,
      "grade_group_students_individually": false,
      "anonymous_peer_reviews": false,
      "group_category_id": null,
      "post_to_sis": false,
      "moderated_grading": false,
      "omit_from_final_grade": false,
      "intra_group_peer_reviews": false,
      "anonymous_instructor_annotations": false,
      "anonymous_grading": false,
      "graders_anonymous_to_graders": false,
      "grader_count": 0,
      "grader_comments_visible_to_graders": true,
      "final_grader_id": null,
      "grader_names_visible_to_final_grader": true,
      "allowed_attempts": -1,
      "annotatable_attachment_id": null,
      "hide_in_gradebook": false,
      "suppress_assignment": false,
      "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6IjZkM2EyYzJmLWQ3ZWQtNDJmYi04ZjljLTZmYzJjYzJlOTg3NCJ9.50R5q3fBp0A4AGZz3VfmboLefXGTA1zs6LJ1fkIl8_Y",
      "lti_context_id": "6d3a2c2f-d7ed-42fb-8f9c-6fc2cc2e9874",
      "course_id": 20354,
      "name": "Y6 - T9 - U2 - L2",
      "submission_types": [
        "online_quiz"
      ],
      "has_submitted_submissions": true,
      "due_date_required": false,
      "max_name_length": 255,
      "in_closed_grading_period": false,
      "graded_submissions_exist": true,
      "user_submitted": false,
      "is_quiz_assignment": true,
      "can_duplicate": false,
      "original_course_id": null,
      "original_assignment_id": null,
      "original_lti_resource_link_id": null,
      "original_assignment_name": null,
      "original_quiz_id": null,
      "workflow_state": "published",
      "important_dates": false,
      "muted": true,
      "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134944",
      "quiz_id": 798605,
      "anonymous_submissions": false,
      "published": true,
      "only_visible_to_overrides": false,
      "visible_to_everyone": true,
      "locked_for_user": false,
      "submissions_download_url": "https://learning.acc.edu.au/courses/20354/quizzes/798605/submissions?zip=1",
      "post_manually": false,
      "anonymize_students": false,
      "require_lockdown_browser": false,
      "restrict_quantitative_data": false
    },
    "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1134944",
    "context_code": "course_20354",
    "context_name": "2025 Year 6 Maths (MPDE)",
    "context_color": null,
    "end_at": "2025-08-03T13:59:59Z",
    "start_at": "2025-08-03T13:59:59Z",
    "url": "https://learning.acc.edu.au/api/v1/calendar_events/assignment_1134944",
    "assignment_overrides": [
      {
        "id": 152878,
        "assignment_id": 1134944,
        "title": "06HR.DE",
        "due_at": "2025-08-03T13:59:59Z",
        "all_day": true,
        "all_day_date": "2025-08-03",
        "unlock_at": "2025-07-19T14:00:00Z",
        "lock_at": "2025-08-10T13:59:59Z",
        "quiz_id": 798605,
        "unassign_item": false,
        "course_section_id": 31629
      }
    ],
    "important_dates": false
  },
  {
    "title": "Y6 - T9 - U1 -  L1",
    "description": "",
    "submission_types": "online_quiz",
    "workflow_state": "published",
    "created_at": "2024-11-20T19:43:02Z",
    "updated_at": "2025-07-21T23:46:58Z",
    "all_day": true,
    "all_day_date": "2025-08-03",
    "id": "assignment_1135193",
    "type": "assignment",
    "assignment": {
      "id": 1135193,
      "description": "",
      "due_at": "2025-08-03T13:59:59Z",
      "unlock_at": "2025-07-19T14:00:00Z",
      "lock_at": "2025-08-10T13:59:59Z",
      "points_possible": 4,
      "grading_type": "points",
      "assignment_group_id": 171921,
      "grading_standard_id": null,
      "created_at": "2024-11-20T19:43:02Z",
      "updated_at": "2025-07-21T23:46:58Z",
      "peer_reviews": false,
      "automatic_peer_reviews": false,
      "position": 1,
      "grade_group_students_individually": false,
      "anonymous_peer_reviews": false,
      "group_category_id": null,
      "post_to_sis": false,
      "moderated_grading": false,
      "omit_from_final_grade": false,
      "intra_group_peer_reviews": false,
      "anonymous_instructor_annotations": false,
      "anonymous_grading": false,
      "graders_anonymous_to_graders": false,
      "grader_count": 0,
      "grader_comments_visible_to_graders": true,
      "final_grader_id": null,
      "grader_names_visible_to_final_grader": true,
      "allowed_attempts": -1,
      "annotatable_attachment_id": null,
      "hide_in_gradebook": false,
      "suppress_assignment": false,
      "secure_params": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6IjlkMmRkZmQyLWQ5MTYtNGRhNy04NzMxLThkNWFlMjcyMGU2MyJ9.L0GutrhSQK005DWp6O1NV5XoZtqoKwY0XruJszgjIp0",
      "lti_context_id": "9d2ddfd2-d916-4da7-8731-8d5ae2720e63",
      "course_id": 20354,
      "name": "Y6 - T9 - U1 -  L1",
      "submission_types": [
        "online_quiz"
      ],
      "has_submitted_submissions": true,
      "due_date_required": false,
      "max_name_length": 255,
      "in_closed_grading_period": false,
      "graded_submissions_exist": true,
      "user_submitted": true,
      "is_quiz_assignment": true,
      "can_duplicate": false,
      "original_course_id": null,
      "original_assignment_id": null,
      "original_lti_resource_link_id": null,
      "original_assignment_name": null,
      "original_quiz_id": null,
      "workflow_state": "published",
      "important_dates": false,
      "muted": true,
      "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1135193",
      "quiz_id": 798854,
      "anonymous_submissions": false,
      "published": true,
      "only_visible_to_overrides": false,
      "visible_to_everyone": true,
      "locked_for_user": false,
      "submissions_download_url": "https://learning.acc.edu.au/courses/20354/quizzes/798854/submissions?zip=1",
      "post_manually": false,
      "anonymize_students": false,
      "require_lockdown_browser": false,
      "restrict_quantitative_data": false
    },
    "html_url": "https://learning.acc.edu.au/courses/20354/assignments/1135193",
    "context_code": "course_20354",
    "context_name": "2025 Year 6 Maths (MPDE)",
    "context_color": null,
    "end_at": "2025-08-03T13:59:59Z",
    "start_at": "2025-08-03T13:59:59Z",
    "url": "https://learning.acc.edu.au/api/v1/calendar_events/assignment_1135193",
    "assignment_overrides": [
      {
        "id": 152875,
        "assignment_id": 1135193,
        "title": "06HR.DE",
        "due_at": "2025-08-03T13:59:59Z",
        "all_day": true,
        "all_day_date": "2025-08-03",
        "unlock_at": "2025-07-19T14:00:00Z",
        "lock_at": "2025-08-10T13:59:59Z",
        "quiz_id": 798854,
        "unassign_item": false,
        "course_section_id": 31629
      }
    ],
    "important_dates": false
  }
]

we will need to extract for each assignment user_submitted, name, html_url, all_day_date, submission_types


I want to use this data to build a web app.  and we will deliver it in three phases.  It should be a modern and sleek SaaS style website like a modern tech startup site.

Phase 1:

The webapp will make the first API call and get a list of lessons that need to be completed in the week through making the series of API above we want to build something like a kanban board or week task calendar where each assignment and lesson is a card on the board.  If the lesson or assignment is outstanding i.e. completion_requirement->completed OR user_submitted is equal to false, it should be gray, if completion_requirement->completed OR user_submitted is equal to true then the card should be green, if 
the task cal will be in the format Monday, Tuesday, Wednesday, Thursday, Friday, Homework

if no days are assigned in the original payload then we will take the lessons in order that they appear in the payloads and assign one per day
if there are days in the original payload then we will put them in the appropriate column.  for example:

based on the original payload this would look like:

Monday, Tuesday, Wednesday, Thursday, Friday, Homework
Spiritual and Physical Fitness unit 3 lesson 11, Spiritual and Physical Fitness unit 3 lesson 12, Spiritual and Physical Fitness unit 3 lesson 13, Spiritual and Physical Fitness unit 3 lesson 14, Spiritual and Physical Fitness unit 3 lesson 15,
Maths Topic 9 lesson B1, Maths Topic 9 lesson B2, Maths Topic 9 lesson B3, Maths Topic 9 lesson B4, Maths Topic 9 lesson B5, assignments
English Unit 11 lesson 1, English Unit 11 lesson 2, English Unit 11 lesson 3, English Unit 11 lesson 4, English Unit 11 lesson 5, assignments
Technology Unit 3 lesson 1, Technology Unit 3 lesson 2, , Technology Unit 3 lesson 3, Technology Unit 3 lesson 4, assignments
 , , Health Unit 3 Lesson 3, , , assignments
 , , PE Unit 3 Lesson 3, , , assignments

 the cards should have a link on them (html_url) and display the other information that we gathered.


 I want to be able to drag and drop lessons/assignment cards between days or homework.


 Phase 2 :

 I want to display the lessons when I click on them rather than link out to them

 to get the lesson content you would need the data returned from the items payload specifically "page_url"

 The API call looks like:


 curl https://learning.acc.edu.au/api/v1/courses/{{course ID}}/pages/{{page_url}}  \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'


 curl https://learning.acc.edu.au/api/v1/courses/20354/pages/topic-6-lets-remember  \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'



The returned payload will look like 

{
  "title": "Topic 6 - Let's Remember",
  "created_at": "2024-11-20T19:43:32Z",
  "url": "topic-6-lets-remember",
  "editing_roles": "teachers",
  "page_id": 2530675,
  "published": true,
  "hide_from_students": false,
  "front_page": false,
  "html_url": "https://learning.acc.edu.au/courses/20354/pages/topic-6-lets-remember",
  "todo_date": null,
  "publish_at": null,
  "updated_at": "2025-07-16T00:59:55Z",
  "locked_for_user": false,
  "body": "<link rel=\"stylesheet\" href=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/9694035/Updated%20Mobile%20CSS%20file21%253A11.css\"><link rel=\"stylesheet\" href=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/1236185/canvas_global_app.css\"><div id=\"kl_wrapper_3\" class=\"kl_wrapper\">\n<div id=\"kl_banner\" class=\"\">\n<h2 class=\"kl_border_radius_5\" style=\"background-color: #023e88; color: #ffffff; padding: 20px 20px 20px 10px;\"><span style=\"font-size: 24pt;\"><strong>&nbsp;<span style=\"font-family: Balsamiq Sans, lato, Helvetica Neue, Helvetica, Arial, sans-serif;\">Topic 6 - Time</span></strong></span></h2>\n</div>\n<div id=\"kl_introduction\" class=\"\" style=\"margin-top: -20px;\">\n<p>&nbsp;</p>\n</div>\n<div id=\"kl_custom_block_1\" class=\"\" style=\"background-color: #e3f6df; color: #023e88;\">\n<h3 class=\"kl_border_radius_5\" style=\"background-color: #45bd2f; color: #000000; margin-top: 0px; padding: 10px; margin-bottom: 20px;\"><span style=\"color: #ffffff;\">&nbsp;<i class=\"fas fa-book\" aria-hidden=\"true\"><span class=\"dp-icon-content\" style=\"display: none;\">&nbsp;</span></i>&nbsp;<span style=\"font-family: Font Awesome 5 Free;\"><strong> </strong>Topic 6 - </span>Let's Remember</span></h3>\n<div class=\"kl_iframe_wrapper kl_iframe_fill_width kl_iframe_responsive_scale kl_iframe_align_center\"><iframe class=\"lti-embed\" style=\"width: 720px; height: 405px; display: inline-block;\" title=\"Y6 Maths V4 Time U1 Let's Remember\" src=\"https://learning.acc.edu.au/courses/20354/external_tools/retrieve?display=borderless&amp;url=https%3A%2F%2Faccde.instructuremedia.com%2Flti%2Flaunch%3Fcustom_arc_launch_type%3Dbare_embed%26custom_arc_media_id%3D4bab159b-d40c-42b7-9762-106f750a42f6-192610%26custom_arc_start_at%3D0\" width=\"720\" height=\"405\" allowfullscreen=\"allowfullscreen\" webkitallowfullscreen=\"webkitallowfullscreen\" mozallowfullscreen=\"mozallowfullscreen\" allow=\"geolocation *; microphone *; camera *; midi *; encrypted-media *; autoplay *; clipboard-write *; display-capture *\" data-studio-resizable=\"true\" data-studio-tray-enabled=\"true\" data-studio-convertible-to-link=\"true\" loading=\"lazy\"></iframe></div>\n<h4 style=\"padding-left: 40px; color: #45bd2f;\"><i class=\"fas fa-paperclip\" aria-hidden=\"true\"><span class=\"dp-icon-content\" style=\"display: none;\">&nbsp;</span></i>&nbsp; <strong><span style=\"color: #023e88; font-size: 14pt;\">Resources</span></strong></h4>\n<p style=\"padding-left: 40px;\"><span style=\"color: #023e88; font-size: 14pt;\">&nbsp; &nbsp; &nbsp; whiteboard, markers, pencil, <strong><a class=\"instructure_file_link instructure_scribd_file inline_disabled\" title=\"6PMTOPIC6 Let's Remember Worksheet.pdf\" href=\"https://learning.acc.edu.au/courses/20354/files/10162880?verifier=9E2sjssGwpE6eZHXEGo3SiqO5mObsW1ZkkSRhGNZ&amp;wrap=1\" target=\"_blank\" data-api-endpoint=\"https://learning.acc.edu.au/api/v1/courses/20354/files/10162880\" data-api-returntype=\"File\"><span style=\"color: #3598db;\">worksheet</span></a></strong></span></p>\n<h4 style=\"padding-left: 40px; color: #45bd2f;\">&nbsp;<i class=\"fas fa-clipboard-list\" aria-hidden=\"true\"><span class=\"dp-icon-content\" style=\"display: none;\">&nbsp;</span></i>&nbsp; <strong><span style=\"color: #023e88; font-size: 14pt;\">Instructions</span></strong></h4>\n<ol>\n<li style=\"list-style-type: none;\">\n<ol style=\"list-style-type: decimal;\">\n<li><span style=\"color: #023e88; font-size: 14pt;\">Watch the video and participate with the teacher</span></li>\n<li><span style=\"color: #023e88; font-size: 14pt;\">Complete 'Let's Remember'</span></li>\n<li><span style=\"color: #023e88; font-size: 14pt;\">Mark using the <a class=\"instructure_file_link instructure_scribd_file inline_disabled\" title=\"6PMTOPIC6 Lets Remember Answers .pdf\" href=\"https://learning.acc.edu.au/courses/20354/files/10162874?verifier=9LaG44aWywMzKYnhniXgVCMMTzpUFn4eRMCiMLBc&amp;wrap=1\" target=\"_blank\" data-api-endpoint=\"https://learning.acc.edu.au/api/v1/courses/20354/files/10162874\" data-api-returntype=\"File\"><strong><span style=\"color: #3598db;\">answers</span></strong></a></span></li>\n<li><span style=\"color: #023e88; font-size: 14pt;\">Identify any clunk points, and work through how to get the correct answer</span></li>\n</ol>\n</li>\n</ol>\n<p><span style=\"color: #023e88;\"><strong><span style=\"color: #3598db;\"><br></span></strong></span><strong></strong></p>\n</div>\n<div id=\"kl_custom_block_4\" class=\"\" style=\"margin-top: -9px;\">\n<p>&nbsp;</p>\n</div>\n</div>\n<p>&nbsp;</p><script src=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/9694034/Updated%20mobile%2021%253A11js.js\"></script><script src=\"https://instructure-uploads-apse2.s3.ap-southeast-2.amazonaws.com/account_134290000000000001/attachments/1341919/BlueCanvasMobileConfig.js\"></script>"
}

we will need to convert this from HTML to JSON using an LLM and then use that to build a content page
obviously we will need the title, html_url and body.

We will need a button to be able to mark the content as done using an API call like this

curl https://learning.acc.edu.au/api/v1/courses/20354/modules/253389/items/2567723/done \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'

which has the format
curl https://learning.acc.edu.au/api/v1/courses/{{courses ID}}/modules/253389/{{modules ID}}/{{items ID}}/done \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'

On the lesson entry we should mark it as read
the API call format for this is
curl https://learning.acc.edu.au/api/v1/courses/{{courses ID}}/modules/253389/{{modules ID}}/{{items ID}}/mark_read \
     -H 'Authorization: Bearer 13429~yBXNnPfKWH2zXUCQWucfNZFNDCUnaTBPDEUHUf7k4rxJX7a7AmnFuaVmMNUC4m4D'


as part of this section I also want to add some dashboard elements to the site, %age of courses complete (progress), marks achieved in assignments etc


Phase 3:

I want to take the PDF that is attached to the phase 2 output and use an LLM to generate a form that the user can complete as part of their completion of the lesson (in this case 6PMTOPIC6 Let's Remember Worksheet.pdf).  the answers are in another attached PDF   6PMTOPIC6 Lets Remember Answers .pdf so we should be able to mark the student responses.

I want to parse the attached video using an LLM and generate a transcript and then use the PDF and the transcript to create something like a RAG and have a chat section on the page with a prompt outlining how the assistant / agent is tutor with expertise in the content and is able to tutor and guide the student in the content but not answer the questions for them directly, only acting as a guide to explain the concepts. 








