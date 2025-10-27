// app.js
document.addEventListener('DOMContentLoaded', () => {
  const shareBtn = document.getElementById('shareBtn');
  const thanks = document.getElementById('thanks');

  // اتصال به Eitaa SDK
  const EitaaWebApp = window.EitaaWebApp || null;

  shareBtn.addEventListener('click', async () => {
    try {
      // درخواست اشتراک شماره از کاربر (مشابه Telegram WebApp)
      const phoneData = await EitaaWebApp.requestPhoneNumber();

      if (phoneData && phoneData.phone_number) {
        const payload = {
          phone: phoneData.phone_number,
          user_id: phoneData.user_id || null
        };

        // ارسال اطلاعات به سرور
        const resp = await fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await resp.json();
        if (data.success) {
          shareBtn.style.display = 'none';
          thanks.style.display = 'block';
        } else {
          alert('خطا در ثبت شماره، لطفاً دوباره تلاش کنید.');
        }
      } else {
        alert('شماره‌ای دریافت نشد. لطفاً مجدداً تلاش کنید.');
      }
    } catch (err) {
      console.error(err);
      alert('امکان اشتراک شماره وجود ندارد.');
    }
  });
});
