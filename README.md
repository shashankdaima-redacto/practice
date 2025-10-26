I'll create a progressive set of Django testing exercises that mirror real-world scenarios you've encountered. These will help you build testing muscle memory and reduce development time.

## 🟢 EASY LEVEL

### Exercise 1: E-commerce Product Catalog

 **Situation** : Building a simple product catalog where products can go out of stock

 **Models** :

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
  
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
  
    @property
    def is_available(self):
        return self.stock > 0
```

 **SDK/Business Logic** :

```python
class InventoryManager:
    def restock_product(self, product, quantity):
        product.stock += quantity
        product.save()
        return product
  
    def process_sale(self, product, quantity):
        if product.stock < quantity:
            raise ValueError("Insufficient stock")
        product.stock -= quantity
        product.save()
        return product
```

 **Tests to Write** :

* Model validation tests
* Property method tests
* Business logic tests with edge cases
* Test database transactions

---

### Exercise 2: Blog Comment System

 **Situation** : Blog with comments that need moderation

 **Models** :

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
  
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Worker Task** (Dramatiq):

```python
@dramatiq.actor
def check_spam_comments():
    """Check unapproved comments for spam"""
    comments = Comment.objects.filter(approved=False)
    for comment in comments:
        if contains_spam_words(comment.content):
            comment.delete()
```

 **Tests to Write** :

* Test worker with mocked spam detection
* Test database state after worker execution
* Test worker error handling

---

## 🟡 MEDIUM LEVEL

### Exercise 3: Subscription Service with Billing

 **Situation** : SaaS platform with monthly subscriptions and automated billing

 **Models** :

```python
class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=dict)
  
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired')
    ])
    next_billing_date = models.DateTimeField()
  
class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
```

 **SDK/Business Logic** :

```python
class BillingService:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway
  
    def process_subscription_payment(self, subscription):
        if subscription.status != 'active':
            raise ValueError("Subscription not active")
      
        payment = Payment.objects.create(
            subscription=subscription,
            amount=subscription.plan.price,
            status='pending'
        )
      
        try:
            result = self.payment_gateway.charge(
                amount=subscription.plan.price,
                customer_id=subscription.user.id
            )
            payment.status = 'completed'
            subscription.next_billing_date += timedelta(days=30)
        except PaymentError:
            payment.status = 'failed'
            subscription.status = 'expired'
      
        payment.save()
        subscription.save()
        return payment
```

 **Scheduler Task** :

```python
def daily_billing_check():
    """Run daily to process due subscriptions"""
    due_subscriptions = Subscription.objects.filter(
        status='active',
        next_billing_date__lte=timezone.now()
    )
  
    service = BillingService(StripeGateway())
    for subscription in due_subscriptions:
        service.process_subscription_payment(subscription)
```

 **Signal Handler** :

```python
@receiver(post_save, sender=Payment)
def notify_payment_service(sender, instance, created, **kwargs):
    if created and instance.status == 'completed':
        # Call external analytics API
        requests.post('https://analytics.example.com/track', json={
            'event': 'payment_completed',
            'amount': str(instance.amount),
            'subscription_id': instance.subscription.id
        })
```

 **Tests to Write** :

* Mock payment gateway in tests
* Test scheduler with time-based scenarios
* Test signal with mocked requests
* Test transaction rollback on failure
* Test concurrent payment processing

---

### Exercise 4: Content Moderation Platform

 **Situation** : Platform where user content needs automated and manual moderation

 **Models** :

```python
class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged')
    ])
    moderation_score = models.FloatField(null=True)
    reviewed_by = models.ForeignKey(User, null=True, related_name='reviews')
  
class ModerationRule(models.Model):
    keyword = models.CharField(max_length=100)
    action = models.CharField(max_length=20)  # 'flag', 'reject', 'review'
    priority = models.IntegerField(default=0)
```

 **Workers** :

```python
@dramatiq.actor(max_retries=3)
def auto_moderate_content(content_id):
    content = Content.objects.get(id=content_id)
  
    # Call ML service for scoring
    score = MLService().analyze_content(content.text)
    content.moderation_score = score
  
    if score > 0.8:
        content.status = 'rejected'
    elif score > 0.5:
        content.status = 'flagged'
        manual_review_queue.send(content_id)
    else:
        content.status = 'approved'
  
    content.save()

@dramatiq.actor
def manual_review_queue(content_id):
    # Assign to available moderator
    moderator = User.objects.filter(
        groups__name='moderators',
        is_active=True
    ).annotate(
        review_count=Count('reviews')
    ).order_by('review_count').first()
  
    if moderator:
        send_review_notification(moderator, content_id)
```

 **Tests to Write** :

* Test worker retry logic
* Test ML service mocking
* Test queue chaining
* Test load balancing logic
* Test race conditions in assignment

---

## 🔴 HARD LEVEL

### Exercise 5: Real-time Order Processing System

 **Situation** : Food delivery platform with real-time order tracking and multi-service integration

 **Models** :

```python
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    is_online = models.BooleanField(default=True)
    preparation_time = models.IntegerField(default=30)  # minutes
  
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery = models.DateTimeField()
    driver = models.ForeignKey(User, null=True, related_name='deliveries')
  
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
  
class OrderEvent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
```

 **Complex Business Logic** :

```python
class OrderOrchestrator:
    def __init__(self):
        self.payment_service = PaymentService()
        self.notification_service = NotificationService()
        self.driver_service = DriverAllocationService()
        self.map_service = MapService()
  
    @transaction.atomic
    def process_order(self, order_data):
        # Create order with items
        order = Order.objects.create(**order_data)
      
        # Process payment
        payment_result = self.payment_service.process(order)
        if not payment_result.success:
            raise PaymentFailedException()
      
        # Schedule workers
        confirm_with_restaurant.send_with_options(
            args=[order.id],
            delay=60000  # 1 minute delay
        )
      
        # Trigger real-time updates
        self.trigger_order_accepted(order)
      
        return order
  
    def trigger_order_accepted(self, order):
        # Find nearest drivers
        drivers = self.driver_service.find_available_drivers(
            order.restaurant.location,
            radius_km=5
        )
      
        for driver in drivers[:10]:
            notify_driver.send(driver.id, order.id)
```

 **Multiple Workers with Dependencies** :

```python
@dramatiq.actor(time_limit=120000)
def confirm_with_restaurant(order_id):
    order = Order.objects.get(id=order_id)
  
    # Call restaurant API
    response = RestaurantAPI().confirm_order(order)
  
    if response.confirmed:
        order.status = 'confirmed'
        order.estimated_delivery = calculate_delivery_time(order)
        order.save()
      
        # Chain next worker
        allocate_driver.send_with_options(
            args=[order.id],
            delay=300000  # 5 minutes before pickup
        )
    else:
        order.status = 'cancelled'
        order.save()
        refund_order.send(order.id)

@dramatiq.actor(max_retries=5)
def allocate_driver(order_id):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)
      
        if order.driver:
            return  # Already allocated
      
        driver = DriverAllocationService().allocate_optimal_driver(order)
        order.driver = driver
        order.save()
      
        # Start tracking
        track_delivery.send(order.id)

@dramatiq.actor
def track_delivery(order_id):
    order = Order.objects.get(id=order_id)
  
    while order.status != 'delivered':
        location = DriverAPI().get_location(order.driver.id)
      
        OrderEvent.objects.create(
            order=order,
            event_type='location_update',
            metadata={'lat': location.lat, 'lng': location.lng}
        )
      
        # Notify customer via websocket
        WebSocketService().send_update(
            f'order_{order.id}',
            {'location': location}
        )
      
        time.sleep(30)  # Update every 30 seconds
        order.refresh_from_db()
```

 **Scheduler Tasks** :

```python
def check_delayed_orders():
    """Run every 5 minutes"""
    delayed_orders = Order.objects.filter(
        status='in_progress',
        estimated_delivery__lt=timezone.now() - timedelta(minutes=10)
    )
  
    for order in delayed_orders:
        # Compensate customer
        create_compensation.send(order.id)
      
        # Alert operations team
        AlertService().send_delay_alert(order)

def daily_analytics_aggregation():
    """Run at midnight"""
    yesterday = timezone.now() - timedelta(days=1)
  
    stats = Order.objects.filter(
        created_at__date=yesterday.date()
    ).aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('total'),
        avg_delivery_time=Avg(
            F('delivered_at') - F('created_at')
        )
    )
  
    # Send to data warehouse
    DataWarehouseAPI().push_daily_stats(stats)
```

 **Complex Signal Handlers** :

```python
@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if instance.status == 'delivered':
        # Multiple API calls
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(
                    CustomerAPI().update_loyalty_points,
                    instance.customer.id,
                    instance.total
                ),
                executor.submit(
                    RestaurantAPI().notify_completion,
                    instance.restaurant.id,
                    instance.id
                ),
                executor.submit(
                    AnalyticsAPI().track_event,
                    'order_completed',
                    instance.to_dict()
                )
            ]
          
            for future in futures:
                future.result()  # Wait for all to complete
```

 **Tests to Write** :

* Test distributed transaction handling
* Test worker failure and retry scenarios
* Test race conditions with select_for_update
* Test concurrent API calls with ThreadPoolExecutor
* Mock multiple external services
* Test websocket notifications
* Test scheduler with time-dependent logic
* Test signal handlers with parallel API calls
* Test worker chaining and delays
* Integration tests for the complete order flow

---

## Testing Best Practices to Apply

For each exercise, focus on:

1. **Setup Optimization** :

* Use `setUpTestData` for read-only test data
* Create factory classes for complex models
* Use fixtures sparingly

1. **Mocking Strategy** :

* Mock external services at the boundary
* Use `unittest.mock.patch` for API calls
* Create test doubles for complex services

1. **Worker Testing** :

* Use `dramatiq.test.StubBroker` for testing
* Test both success and failure paths
* Verify message queuing and delays

1. **Signal Testing** :

* Temporarily disconnect signals when not testing them
* Use `override_settings` for signal configuration
* Test async signal handlers separately

1. **Performance** :

* Use `assertNumQueries` to catch N+1 problems
* Profile slow tests with `pytest-profiling`
* Parallelize tests with `pytest-xdist`

Start with Easy exercises to build confidence, then gradually move to harder ones. Each exercise builds on concepts from the previous ones, helping you develop a comprehensive testing skillset that will significantly reduce your development time.
