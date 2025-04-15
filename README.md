Project Description

The Forum System API is a RESTful API designed for a forum platform, enabling users to interact through topics, replies, messages, and categories, with administrative controls for managing content and access. The API supports a range of functionalities, from user authentication and topic creation to private category management and voting on replies. It is built to be consumed by various clients, ensuring flexibility and scalability.

Key Features:

Users: Register, log in, create topics/replies, send messages, and vote on replies.

Administrators: Manage users, categories, topics, and access permissions.

Core Resources: Users, Topics, Categories, Replies, and Messages.

Authentication: Token-based access for secure endpoints.

Flexibility: Supports search, sort, pagination, and private category controls.

Requirements:

MUST Requirements:

Token Endpoint:
Accepts user login data (e.g., username/password).
Returns an authentication token for accessing protected endpoints.

Register User:
Accepts user registration data (e.g., username, email, password).
Ensures at least one unique property (e.g., username or email) for login.

Create Topic:
Requires authentication.
Needs a title and a category.

Create Reply:
Requires authentication.
Includes text and associates with a specific topic.

View Topics:
Returns a list of topics.
Supports search, sort, and pagination query parameters.

View Topic:
Returns a single topic with its replies.

View Category:
Lists all topics in a category.
Supports search, sort, and pagination.

View Categories:
Returns a list of all categories.

Create Message:
Requires authentication.
Creates a message with text, addressed to a specific user.

View Conversation:
Requires authentication.
Shows messages exchanged between the authenticated user and another user.

View Conversations:
Requires authentication.
Lists all users with whom the authenticated user has messaged.

Upvote/Downvote a Reply:
Requires authentication.
Allows users to upvote or downvote a reply once, with the ability to change their vote.

Choose Best Reply:
Requires authentication.
Allows the topic author to select one best reply.


SHOULD Requirements:

Create Category:
Requires admin authentication.
Needs at least a name.
Make Category Private/Non-private:
Requires admin authentication.
Toggles category visibility; private categories are accessible only to members.

Give User Category Read Access:
Requires admin authentication.
Grants a user access to view topics and replies in a private category.

Give User Category Write Access:
Requires admin authentication.
Allows a user to view and post topics/replies in a private category.

Revoke User Access:
Requires admin authentication.
Removes a user’s read or write access to a category.

View Privileged Users:
Requires admin authentication.
Lists users with their access levels for a private category.

Lock Topic:
Requires admin authentication.
Prevents new replies to a topic.

Lock Category:
Requires admin authentication.
Prevents new topics in a category.


COULD Requirements:

Create a Client:
Develop a client (e.g., web or mobile) to consume the API.