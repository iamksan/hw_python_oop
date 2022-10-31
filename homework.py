from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        "Тип тренировки: {}; "
        "Длительность: {:.3f} ч.; "
        "Дистанция: {:.3f} км; "
        "Ср. скорость: {:.3f} км/ч; "
        "Потрачено ккал: {:.3f}."
    )

    def get_message(self) -> None:
        t = asdict(self)
        return self.MESSAGE.format(*t.values())


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    k_1: int = 18
    k_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (self.k_1 * self.get_mean_speed() - self.k_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    k_1: float = 0.035
    k_2: int = 2
    k_3: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.k_1 * self.weight
                + (self.get_mean_speed() ** self.k_2 // self.height)
                * self.k_3
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    k_1: float = 1.1
    k_2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        c_p = self.count_pool
        l_p = self.lenght_pool
        return l_p * c_p / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.k_1) * self.k_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_class = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return train_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    message_train = training.show_training_info()
    print(message_train.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
