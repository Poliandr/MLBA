import time
import pandas as pd
import matplotlib.pyplot as plt
import os

# Пути к файлам логов и картинки гистограммы
log_file = '/app/logs/metric_log.csv'
output_file = '/app/logs/error_distribution.png'

# Цикл постоянной отрисовки гистограммы
while True:
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file)
            if len(df) > 0:
                plt.figure()
                plt.hist(df['absolute_error'], bins=20)
                plt.title("Absolute Error Distribution")
                plt.xlabel("Absolute Error")
                plt.ylabel("Frequency")
                plt.savefig(output_file)
                plt.close()
                print("Гистограмма обновлена.")
            else:
                print("Файл metric_log.csv пуст.")
        except Exception as e:
            print(f"Ошибка при построении гистограммы: {e}")
    else:
        print("Файл metric_log.csv не найден.")
    # Интервал обновления гистограммы
    time.sleep(10)
