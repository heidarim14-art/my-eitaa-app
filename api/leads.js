// api/leads.js
import { sql } from '@vercel/postgres';

export default async function handler(req, res) {
  // فقط درخواست‌های POST را قبول کن
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method Not Allowed' });
  }

  try {
    const { user_id, phone } = req.body;
    if (!phone) {
      return res.status(400).json({ success: false, error: 'Phone missing' });
    }

    // ۱. ساخت جدول (اگر وجود نداشته باشد)
    // این دستور فقط بار اول اجرا می‌شود
    await sql`
      CREATE TABLE IF NOT EXISTS leads (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        phone TEXT UNIQUE, 
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // ۲. درج اطلاعات در دیتابیس
    // ON CONFLICT (phone) DO NOTHING: اگر شماره تکراری بود، خطا نده و رد شو
    await sql`
      INSERT INTO leads (user_id, phone)
      VALUES (${user_id || null}, ${phone})
      ON CONFLICT (phone) DO NOTHING;
    `;

    // ۳. ارسال پاسخ موفقیت‌آمیز به کلاینت (app.js)
    res.status(200).json({ success: true });

  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: err.message });
  }
}