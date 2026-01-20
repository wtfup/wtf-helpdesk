<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <div class="bg-gradient-to-br from-wtf-dark to-gray-900 text-white">
      <div class="max-w-5xl mx-auto px-6 py-16 text-center">
        <!-- Logo -->
        <div class="flex justify-center mb-6">
          <img
            src="/assets/helpdesk/images/wtf-logo-white.png"
            alt="WTF Support"
            class="h-12"
            onerror="this.style.display='none'"
          />
        </div>

        <h1 class="text-4xl font-bold mb-4">How can we help you?</h1>
        <p class="text-lg text-gray-300 mb-8">
          Search our knowledge base or submit a support ticket
        </p>

        <!-- Search Bar -->
        <div class="max-w-2xl mx-auto">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search for articles, guides, FAQs..."
              class="w-full px-6 py-4 rounded-xl text-gray-900 text-lg focus:outline-none focus:ring-4 focus:ring-wtf-orange/30 shadow-lg"
              @keyup.enter="handleSearch"
            />
            <button
              @click="handleSearch"
              class="absolute right-3 top-1/2 -translate-y-1/2 bg-wtf-orange hover:bg-wtf-orange/90 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Search
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="max-w-5xl mx-auto px-6 -mt-8">
      <div class="grid md:grid-cols-2 gap-6">
        <!-- Submit Ticket Card -->
        <router-link
          to="/helpdesk/my-tickets/new"
          class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow group"
        >
          <div class="flex items-start gap-4">
            <div class="bg-wtf-orange/10 p-3 rounded-lg group-hover:bg-wtf-orange/20 transition-colors">
              <svg class="w-8 h-8 text-wtf-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-semibold text-gray-900 mb-1">Submit a Ticket</h3>
              <p class="text-gray-600">Can't find what you're looking for? Create a support ticket and our team will help you.</p>
            </div>
          </div>
        </router-link>

        <!-- My Tickets Card -->
        <router-link
          to="/helpdesk/my-tickets"
          class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow group"
        >
          <div class="flex items-start gap-4">
            <div class="bg-blue-100 p-3 rounded-lg group-hover:bg-blue-200 transition-colors">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-semibold text-gray-900 mb-1">My Tickets</h3>
              <p class="text-gray-600">View and track the status of your existing support requests.</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Knowledge Base Section -->
    <div class="max-w-5xl mx-auto px-6 py-12">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Knowledge Base</h2>

      <div class="grid md:grid-cols-3 gap-6" v-if="categories.data?.length">
        <router-link
          v-for="category in categories.data"
          :key="category.name"
          :to="`/helpdesk/kb-public/${category.name}`"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition-shadow border border-gray-100"
        >
          <div class="flex items-center gap-3 mb-3">
            <span class="text-2xl">{{ category.icon || '📚' }}</span>
            <h3 class="text-lg font-semibold text-gray-900">{{ category.category_name }}</h3>
          </div>
          <p class="text-gray-600 text-sm" v-if="category.description">
            {{ category.description }}
          </p>
          <p class="text-gray-500 text-sm mt-2">
            {{ category.article_count || 0 }} articles
          </p>
        </router-link>
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        <p>Knowledge base categories are being set up...</p>
      </div>
    </div>

    <!-- Contact Info Section -->
    <div class="bg-gray-100 py-12">
      <div class="max-w-5xl mx-auto px-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">Other Ways to Reach Us</h2>

        <div class="grid md:grid-cols-3 gap-6">
          <!-- Email -->
          <div class="bg-white rounded-xl p-6 text-center">
            <div class="bg-gray-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900 mb-1">Email</h3>
            <p class="text-gray-600">support@wtfgyms.com</p>
          </div>

          <!-- Phone -->
          <div class="bg-white rounded-xl p-6 text-center">
            <div class="bg-gray-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900 mb-1">Phone</h3>
            <p class="text-gray-600">Available in-app</p>
          </div>

          <!-- Hours -->
          <div class="bg-white rounded-xl p-6 text-center">
            <div class="bg-gray-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="font-semibold text-gray-900 mb-1">Support Hours</h3>
            <p class="text-gray-600">24/7 for Premium</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-wtf-dark text-white py-8">
      <div class="max-w-5xl mx-auto px-6 text-center">
        <p class="text-gray-400">&copy; {{ new Date().getFullYear() }} WTF Gyms. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { createListResource } from "frappe-ui";
import { capture } from "@/telemetry";

const router = useRouter();
const searchQuery = ref("");

// Fetch KB categories
const categories = createListResource({
  doctype: "HD Article Category",
  fields: ["name", "category_name", "description", "icon"],
  filters: {
    published: 1,
  },
  orderBy: "idx asc",
  pageLength: 9,
  auto: true,
  transform: (data) => {
    return data.map((cat: any) => ({
      ...cat,
      article_count: 0, // Could be enhanced to show actual count
    }));
  },
});

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: "/helpdesk/kb-public",
      query: { q: searchQuery.value },
    });
  }
};

onMounted(() => {
  capture("support_home_viewed");
});
</script>

<style scoped>
/* WTF Brand Colors */
.bg-wtf-dark {
  background-color: #1a1a2e;
}

.bg-wtf-orange {
  background-color: #ff6b35;
}

.hover\:bg-wtf-orange\/90:hover {
  background-color: rgba(255, 107, 53, 0.9);
}

.text-wtf-orange {
  color: #ff6b35;
}

.bg-wtf-orange\/10 {
  background-color: rgba(255, 107, 53, 0.1);
}

.bg-wtf-orange\/20 {
  background-color: rgba(255, 107, 53, 0.2);
}

.focus\:ring-wtf-orange\/30:focus {
  --tw-ring-color: rgba(255, 107, 53, 0.3);
}

.from-wtf-dark {
  --tw-gradient-from: #1a1a2e;
}
</style>
