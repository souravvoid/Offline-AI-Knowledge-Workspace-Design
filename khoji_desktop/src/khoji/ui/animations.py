from __future__ import annotations

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPoint,
    QTimer,
)
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect


def fade_in(
    widget: QWidget,
    duration: int = 220,
    delay: int = 0,
    on_finished: callable = None,
) -> QPropertyAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    effect.setOpacity(0.0)
    widget.show()

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    if delay > 0:
        QTimer.singleShot(delay, anim.start)
    else:
        anim.start()

    if on_finished:
        anim.finished.connect(on_finished)

    return anim


def fade_out(
    widget: QWidget,
    duration: int = 180,
    delay: int = 0,
    on_finished: callable = None,
) -> QPropertyAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    effect.setOpacity(1.0)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(1.0)
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    if delay > 0:
        QTimer.singleShot(delay, anim.start)
    else:
        anim.start()

    if on_finished:
        anim.finished.connect(on_finished)

    return anim


def slide_in(
    widget: QWidget,
    direction: str = "up",
    distance: int = 20,
    duration: int = 250,
    delay: int = 0,
) -> QPropertyAnimation:
    orig = widget.pos()
    start = QPoint(orig.x(), orig.y())
    if direction == "up":
        start.setY(orig.y() + distance)
    elif direction == "down":
        start.setY(orig.y() - distance)
    elif direction == "left":
        start.setX(orig.x() + distance)
    elif direction == "right":
        start.setX(orig.x() - distance)

    widget.move(start)
    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duration)
    anim.setStartValue(start)
    anim.setEndValue(orig)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    if delay > 0:
        QTimer.singleShot(delay, anim.start)
    else:
        anim.start()

    return anim


def stagger_fade_in(
    widgets: list[QWidget],
    stagger_ms: int = 100,
    fade_duration: int = 200,
) -> QParallelAnimationGroup:
    group = QParallelAnimationGroup()
    for i, w in enumerate(widgets):
        effect = QGraphicsOpacityEffect(w)
        w.setGraphicsEffect(effect)
        effect.setOpacity(0.0)
        w.show()

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(fade_duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.setStartTime(i * stagger_ms)
        group.addAnimation(anim)

    group.start()
    return group


def pulse_glow(
    widget: QWidget,
    duration: int = 1500,
    repeat: bool = True,
) -> QPropertyAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.6)
    anim.setKeyValueAt(0.5, 1.0)
    anim.setEndValue(0.6)
    anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    if repeat:
        anim.setLoopCount(-1)

    anim.start()
    return anim


def sequence_animations(animations: list) -> QSequentialAnimationGroup:
    group = QSequentialAnimationGroup()
    for a in animations:
        group.addAnimation(a)
    return group


def parallel_animations(animations: list) -> QParallelAnimationGroup:
    group = QParallelAnimationGroup()
    for a in animations:
        group.addAnimation(a)
    return group
