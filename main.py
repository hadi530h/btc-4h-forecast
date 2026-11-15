import json
import os
import glob

def get_forecast(prices):
    last_price = prices[-1]
    # نستخدم آخر 240 دقيقة (4 ساعات) لحساب الاتجاه المحلي
    n = min(240, len(prices))
    subset = prices[-n:]
    
    # حساب الانحدار الخطي البسيط: y = mx + b
    sum_x = sum(range(n))
    sum_y = sum(subset)
    sum_xy = sum(i * subset[i] for i in range(n))
    sum_x2 = sum(i * i for i in range(n))
    
    denom = n * sum_x2 - sum_x * sum_x
    if denom == 0:
        return last_price
        
    m = (n * sum_xy - sum_x * sum_y) / denom
    
    # تخميد الاتجاه (Shrinkage) لتجنب المبالغة في التوقع بسبب ضوضاء السوق
    # التوقع الكامل سيكون last_price + m * 240، لكننا نضربه في 0.15 للأمان
    shrinkage = 0.15
    forecast = last_price + (m * 240 * shrinkage)
    
    return max(0.00001, forecast) # ضمان أن السعر أكبر من صفر

def main():
    input_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    
    # معالجة جميع ملفات الحالة بترتيب أبجدي
    for filepath in sorted(glob.glob(os.path.join(input_dir, "*.in"))):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        case_id = data["case"]
        prices = data["markets"][0]["prices"]
        
        forecast = get_forecast(prices)
        
        result = {
            "forecasts": [{
                "case": case_id, 
                "price": round(forecast, 5)
            }]
        }
        
        out_path = os.path.join(output_dir, f"{case_id}.out")
        with open(out_path, 'w', encoding='utf-8') as f:
            # استخدام separators لإخراج JSON مضغوط بدون مسافات زائدة
            json.dump(result, f, separators=(',', ':'))

if __name__ == "__main__":
    main()
