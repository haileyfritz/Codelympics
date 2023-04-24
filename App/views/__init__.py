# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .coordinator import coordinator_views
from .auth import auth_views


views = [user_views, index_views, auth_views, coordinator_views] 
# blueprints must be added to this list