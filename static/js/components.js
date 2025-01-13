export const createFooter = () => {
    return `
        <footer class="bg-dark-secondary py-6 mt-auto">
            <div class="container mx-auto px-8">
                <div class="flex justify-between items-center">
                    <div class="text-sm text-gray-400">
                        © 2025 myDashboard by HanSeongJun
                    </div>
                    <div class="flex items-center gap-4">
                        <a href="https://github.com/daybreaker42/mydashboard" 
                           class="hover:text-blue-400 transition-colors flex items-center gap-2">
                            <img src="/static/assets/github-mark-white.svg" alt="GitHub" class="w-5 h-5">
                            GitHub
                        </a>
                        <a href="/static/licenses.txt" class="hover:text-blue-400 transition-colors">
                            Licenses
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    `;
};

export const createHeader = () => {
    return `
        <nav class="bg-dark-secondary">
            <div class="container mx-auto px-8 py-4 flex justify-between items-center">
                <a href="/" class="text-2xl font-bold hover:text-blue-400 transition-colors">myDashboard</a>
                <div class="flex items-center gap-6">
                    <a href="/markets" class="hover:text-blue-400 transition-colors">Markets</a>
                    <a href="/about" class="hover:text-blue-400 transition-colors">About</a>
                </div>
            </div>
        </nav>
    `;
};
