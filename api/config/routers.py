from rest_framework.routers import SimpleRouter

from vet.viewsets import ClientViewSet, AppointmentViewSet


router = SimpleRouter()


router.register(r"client", ClientViewSet, "client")
router.register(r"appointment", AppointmentViewSet, "appointment")
