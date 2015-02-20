
def get_click_tile(click, render_coof,map):
    '''
    Функция, определяющая, по какому тайлу кликнули мышью.
    Если клик за пределами сцены - находит ближайшую точку (это не работает для недосупных мест на самой карте)
    '''
    cor = [click[0]-render_coof[0],click[1]-render_coof[1]]
    x = 0
    y = 0
    while cor[0] >100:
        cor[0] -= 100
        x+=1
    while cor[1] >100:
        cor[1] -= 100
        y+=1
    if x >= len(map[0]):
        x = len(map[0])-1
    if y >= len(map):
        y = len(map)-1
    return (x,y)