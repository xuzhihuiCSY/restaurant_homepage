# Restaurant Website Implementation Plan / 餐厅网站开发实施方案

This document outlines the technical implementation plan for a responsive restaurant homepage built with Django-rendered HTML templates. The page highlights restaurant information, restaurant photos, today's recommended dishes, owner-written review highlights, upcoming events, and basic contact/location details.

本文件概述 food/餐饮 网站首页的开发实施方案。项目采用 Django + HTML 模板实现，不做前后端分离。首页只展示餐厅介绍、餐厅照片、今日推荐菜、owner 手动填写的评价展示、近期活动、联系方式与地址信息，不承载完整菜单。

---

## 1. System Architecture / 系统架构

A simple Django monolithic architecture is sufficient for a restaurant homepage. Django handles routing, database access, server-side rendering, static assets, and administration in one project.
餐厅首页不需要复杂的前后端分离架构。采用简单的 Django 单体架构即可：由 Django 统一处理路由、数据库访问、服务端 HTML 渲染、静态资源和后台管理。

* **Application Framework (应用框架):** Django
    * Provides a powerful, out-of-the-box Administrative Panel for the owner to securely manage content.
    * 内置功能强大的管理后台（Django Admin），供餐厅所有者安全地管理网站内容。
    * Renders homepage HTML directly through Django views and templates.
    * 通过 Django 视图和模板直接渲染首页 HTML。
* **Frontend Assets (前端资源):** HTML Templates + CSS + Minimal JavaScript
    * Uses Django templates for page structure and static CSS/JS for responsive layout and lightweight interactions.
    * 使用 Django 模板组织页面结构，通过静态 CSS/JS 实现响应式布局和少量交互。
* **Database (数据库):** SQLite (Development / Small Deployment)
    * Relational database to maintain homepage content, daily recommendations, pricing, and event details.
    * 关系型数据库，用于维护首页内容、今日推荐菜、价格和活动信息。

---

## 2. Core Feature Specifications / 核心功能规范

### 2.1 Public Homepage (Read-Only) / 公开首页（只读）
* **Hero Section (首页首屏):** Displays the restaurant name, core selling point, opening status, and primary call-to-action such as viewing today's recommendations or calling the restaurant.
    * 展示餐厅名称、核心卖点、营业状态，以及查看今日推荐菜或拨打电话等主要操作入口。
* **Today's Recommended Dishes (今日推荐菜):** Displays a small curated list of dishes for the current day. This is not a full menu.
    * 展示当天精选的少量推荐菜品，不展示完整菜单。
* **Review Highlights (评价展示):** Displays owner-written review highlights between recommendations and events. There is no public customer submission flow.
    * 在今日推荐菜和活动之间展示 owner 手动填写的评价内容，不提供公开用户提交评论功能。
* **Restaurant Photo Display (餐厅照片展示):** Displays owner-managed restaurant photos between the hero section and today's recommendations.
    * 在首页首屏和今日推荐菜之间展示 owner 管理的餐厅照片。
* **Optional Online Order Section (可选在线点餐区):** Displays a single "Order Online" button when the owner enables the section and provides an online order URL.
    * 当 owner 开启该区块并提供在线点餐链接时，显示一个 “Order Online” 按钮。
* **Upcoming Events List (近期活动列表):** A simple homepage list displaying community events, holiday specials, or live music scheduled at the venue.
    * 简洁列表展示餐厅计划举办的社区活动、节日特惠或现场音乐会。
* **Contact & Location Section (联系方式与地址):** Displays phone number, email, address, opening hours, and an optional embedded map link. The owner can choose whether the hero contact button prioritizes phone or email.
    * 展示电话、邮箱、地址、营业时间，以及可选的地图链接。Owner 可以选择首页首屏联系按钮优先使用电话或邮箱。
* **Mobile-First Responsive Design (移动端优先响应式设计):** Highly optimized layout for smartphones, as the majority of restaurant patrons check menus on mobile web browsers.
    * 针对智能手机进行高度优化，因为绝大多数餐厅顾客都会使用手机浏览器查看菜单。

### 2.2 Owner Administration Panel (Read/Write) / 商家管理后台（读写）
* **Secure Authentication (安全身份验证):** Access limited strictly to users with `is_staff` or `is_superuser` flags using Django's native session-based authentication. General site visitors cannot view or access this path.
    * 利用 Django 原生的 Session 身份验证，访问权限严格限制为具有 `is_staff` 或 `is_superuser` 标签的用户。普通访客无法查看或访问此路径。
* **Owner Control Dashboard (Owner 控制界面):** A protected `/owner/` dashboard for updating restaurant information, managing restaurant photos, maintaining today's recommended dishes, writing review highlights, setting discounts, and scheduling events without writing code.
    * 提供受保护的 `/owner/` 控制界面，供所有者在不编写代码的情况下更新餐厅信息、管理餐厅照片、维护今日推荐菜、手动填写评价展示、设置折扣以及安排活动。
* **Availability & Promotion Toggles (供应状态与促销开关):** Quick checkboxes to hide unavailable recommendations or mark a recommendation as on sale with a discount price.
    * 快捷复选框，可隐藏不可供应的推荐菜，或为推荐菜设置折扣价。
* **Django Admin Fallback (Django Admin 备用后台):** Django Admin remains available for advanced staff-level data management.
    * Django Admin 仍可作为高级数据管理备用入口。

---

## 3. Database Data Models / 数据库数据模型

The Django app uses a small set of models to power the homepage content:
Django 应用使用少量模型支持首页内容展示：

### RestaurantProfile Model (餐厅信息模型)
* `name` (CharField): Restaurant name.
* `tagline` (CharField): Short homepage slogan.
* `description` (TextField): Introductory copy.
* `phone` (CharField): Contact phone number.
* `email` (EmailField): Contact email address.
* `primary_contact_method` (CharField): Chooses whether the hero contact button prioritizes phone or email.
* `address` (CharField): Restaurant address.
* `opening_hours` (CharField): Business hours.
* `map_url` (URLField): Optional map link.
* `show_online_order` (BooleanField): Toggles whether the online order section is visible.
* `online_order_url` (URLField): Required when `show_online_order` is True.
* `hero_image` (ImageField): Homepage hero image.

### DailyRecommendation Model (今日推荐菜模型)
* `name` (CharField): Name of the dish.
* `description` (TextField): Ingredients, allergies, or item details.
* `price` (DecimalField): Regular price.
* `display_date` (DateField): Date when the dish should appear on the homepage.
* `is_available` (BooleanField): Toggles whether the recommendation is visible.
* `is_on_sale` (BooleanField): Toggles display of a promotional price.
* `sale_price` (DecimalField, optional): Promotional price when `is_on_sale` is True.
* `image` (ImageField): Photo of the dish.
* `order` (IntegerField): Display order for today's recommendations.

### RestaurantPhoto Model (餐厅照片模型)
* `title` (CharField): Optional photo caption.
* `image` (ImageField): Restaurant photo.
* `is_visible` (BooleanField): Toggles whether the photo appears on the homepage.
* `order` (IntegerField): Display order for the photo section.

### CustomerReview Model (评价展示模型)
* `customer_name` (CharField): Display name entered by the owner.
* `quote` (TextField): Review text entered by the owner.
* `rating` (PositiveSmallIntegerField): Displayed rating from 1 to 5.
* `is_visible` (BooleanField): Toggles whether the highlight appears on the homepage.
* `order` (IntegerField): Display order for the review highlight section.

### Event Model (活动模型)
* `title` (CharField): Event headline (e.g., "Live Jazz Night").
* `description` (TextField): Event breakdown and reservation rules.
* `event_date` (DateField): Event date shown on the homepage.
* `start_time` (TimeField): Start timing.
* `cover_image` (ImageField): Promotional banner.

---

## 4. Development Roadmap / 开发时间线与路线图

* **Phase 1: Django Setup & Models / 第一阶段：Django 项目搭建与模型设计**
    * Initialize the Django project and homepage app. Create database models for restaurant profile information, restaurant photos, daily recommendations, customer reviews, and events.
    * 初始化 Django 项目和首页应用。创建餐厅基础信息、餐厅照片、今日推荐菜、顾客评价和活动模型。
* **Phase 2: Admin & Content Management / 第二阶段：后台管理与内容维护**
    * Build an owner-friendly dashboard and keep Django Admin available for advanced management.
    * 开发面向 owner 的控制界面，并保留 Django Admin 作为高级管理入口。
* **Phase 3: HTML Template Homepage / 第三阶段：首页 HTML 模板开发**
    * Build the homepage with Django templates, static CSS, and minimal JavaScript for navigation, responsive behavior, and simple interactions.
    * 使用 Django 模板、静态 CSS 和少量 JavaScript 开发首页，实现导航、响应式布局和基础交互。
* **Phase 4: Testing & Launch / 第四阶段：测试与上线**
    * Verify homepage rendering, mobile layout, admin access control, image uploads, and basic SEO metadata before deployment.
    * 上线前检查首页渲染、移动端布局、后台访问权限、图片上传和基础 SEO 元信息。
