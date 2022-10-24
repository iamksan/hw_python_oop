class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        print(f'''
        Тип тренировки: {self.training_type};
        Длительность: {self.duration:.3f} ч.;
        Дистанция: {self.distance:.3f} км;
        Ср. скорость: {self.speed:3f} км/ч;
        Потрачено ккал: {self.calories:.3f}.
        ''')


class Training:        
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight         

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        M_IN_KM = 1000
        return self.action * self.LEN_STEP / M_IN_KM
        
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, 
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
    
    def get_spent_calories(self):
        M_IN_KM = 1000
        MINUTES_IN_HOUR = 60
        MIN_IN_HOUR = self.duration * MINUTES_IN_HOUR
        K1 = self.CALORIES_MEAN_SPEED_MULTIPLIER
        K2 = self.CALORIES_MEAN_SPEED_SHIFT = 1.79
        mean_speed = self.get_mean_speed()
        return ((K1 * mean_speed + K2) * self.weight / M_IN_KM * MIN_IN_HOUR)

    
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        K1 = 0.035
        K2 = 0.029
        weight = self.weight
        m_s = self.get_mean_speed()
        MINUTES_IN_HOUR = 60
        height = self.height
        MIN_IN_HOUR = self.duration * MINUTES_IN_HOUR
        return ((K1 * weight + (m_s**2 // height) * K2 * weight) * MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM = 1000
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = 1.38
    
    def get_distance(self) -> float:
        return round(self.action * self.LEN_STEP / self.M_IN_KM)
    
    def get_mean_speed(self) -> float:
        l_p = self.length_pool
        c_p = self.count_pool
        duration = self.duration
        return l_p * c_p // self.M_IN_KM // duration
    
    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration




def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_class = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return train_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

