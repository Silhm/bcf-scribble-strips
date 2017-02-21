<template>
    <div class=knob-wrapper>
      <div class="knob-name"> {{ knobname }}</div>
      <div class="knob-surround"> 
        <div class="knob" v-on:mousewheel="mouseScroll" v-on:click="mouseScroll" v-draw-knob="{ knobtype: knobtype }" v-bind:style="rotationStyle"></div> 
        <span class="min">Min</span> 
        <span class="max">Max</span> 
        <div class="ticks"> 
          <div v-for="tick in ticks" class="tick" v-bind:class="{ activetick: tick }"></div>
        </div>
        <div class="percent">{{ percent }} %</div> 
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      rotationStyle: {
        '-moz-transform': 'rotate(0deg)',
        '-webkit-transform': 'rotate(0deg)',
        '-o-transform': 'rotate(0deg)',
        '-ms-transform': 'rotate(0deg)',
        'transform': 'rotate(0deg)'
      },
      angle: 0,
      percent: 0,
      ticks: new Array(28),
      minangle: 0,
      maxangle: 270,
      minvol: -200,
      maxvol: 6,
      mingain: -20,
      maxgain: 20,
      width: 150,
      height: 150
    }
  },
  props: {
    knobname: String,
    knobtype: {
      type: String,
      default: 'standard'
    },
    val: {
      type: Number,
      default: 0
    }
  },
  computed: {
    dBVal: function () {
      return this.val
    }
  },
  watch: {
    val: function (newVal, oldVal) {
      console.log(newVal)
      if (this.knobtype === 'pan') {
        this.setAngle(this.maxangle * newVal)
      } else if (this.knobtype === 'vol') {
        var volval = (newVal - this.minvol + 1) / (this.maxvol - this.minvol + 1)
        // this.setAngle(this.maxangle * volval);
        this.setAngle(20 * Math.log10(this.maxangle * volval))
      } else if (this.knobtype === 'trim') {
        var trimval = (newVal - this.mingain) / (this.maxgain - this.mingain)
        this.setAngle(this.maxangle * trimval)
      } else {
        this.setAngle(0)
      }
    }
  },
  directives: {
    drawKnob: function (elem, binding) {

    }
  },
  methods: {
    mouseScroll: function (e) {
      if (e.deltaY > 0) {
        this.moveKnob('down')
      } else {
        this.moveKnob('up')
      }
      return false
    },

    moveKnob (direction) {
      if (direction === 'up') {
        if ((this.angle + 2) <= this.maxangle) {
          this.setAngle(this.angle + 2)
        }
      } else if (direction === 'down') {
        if ((this.angle - 2) >= this.minangle) {
          this.setAngle(this.angle - 2)
        }
      }
    },

    setAngle (angle) {
      this.angle = angle
      this.rotationStyle['transform'] = 'rotate(' + angle + 'deg)'
      this.percent = Math.round((angle / 270) * 100)
      // rotate knob

      // highlight ticks
      var activeTicks = (Math.round(this.angle / 10) + 1)

      for (var i = 0; i < this.ticks.length; i++) {
        if (this.knobtype === 'pan') {
          this.ticks[i] = false
          this.ticks[activeTicks] = true
        } else {
          this.ticks[i] = i < activeTicks
        }
      }
    }
  }
}
</script>
<style scoped>

@import url(http://fonts.googleapis.com/css?family=Varela+Round|Open+Sans:300);


.knob-wrapper{
    margin: 2em auto 5em auto;
    }
.knob-name{
	margin-bottom: 1em;
	opacity: .5;
}

.knob-surround {
  position: relative;
  background-color: grey;
  width: 2em;
  height: 2em;
  border-radius: 50%;
  border: solid 0.25em #0e0e0e;
  margin: auto;
  background: #181818;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #1d1d1d), color-stop(1, #131313));
  background: -ms-linear-gradient(bottom, #1d1d1d, #131313);
  background: -moz-linear-gradient(center bottom, #1d1d1d 0%, #131313 100%);
  background: -o-linear-gradient(#131313, #1d1d1d);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#131313', endColorstr='#1d1d1d', GradientType=0);
  -webkit-box-shadow: 0 0.2em 0.1em 0.05em rgba(255, 255, 255, 0.1) inset, 0 -0.2em 0.1em 0.05em rgba(0, 0, 0, 0.5) inset, 0 0.5em 0.65em 0 rgba(0, 0, 0, 0.3);
  -moz-box-shadow: 0 0.2em 0.1em 0.05em rgba(255, 255, 255, 0.1) inset, 0 -0.2em 0.1em 0.05em rgba(0, 0, 0, 0.5) inset, 0 0.5em 0.65em 0 rgba(0, 0, 0, 0.3);
  box-shadow: 0 0.2em 0.1em 0.05em rgba(255, 255, 255, 0.1) inset, 0 -0.2em 0.1em 0.05em rgba(0, 0, 0, 0.5) inset, 0 0.5em 0.65em 0 rgba(0, 0, 0, 0.3);
}
.knob {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  transform: rotate(0deg);
  z-index: 10;
}
.knob:before {
  content: "";
  position: absolute;
  bottom: 19%;
  left: 19%;
  width: 5%;
  height: 5%;
  background-color: #a8d8f8;
  border-radius: 50%;
}
.min,
.max,
.percent {
  display: block;
  font-family: "Varela Round", sans-serif;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  -webkit-font-smoothing: antialiased;
  font-size: 70%;
  position: absolute;
  opacity: .5;
}
.min {
  bottom: -3em;
  left: -2.5em;
}
.max {
  bottom: -3em;
  right: -2.5em;
}
.percent {
  bottom: -4.5em;
}
.tick {
  position: absolute;
  width: 100%;
  height: 50%;
  top: 10px;
  left: 0;
  z-index: 5;
  overflow: visible;
}
.tick:after {
  content: "";
  width: .08em;
  height: .6em;
  background-color: rgba(255, 255, 255, 0.2);
  position: absolute;
  top: -1.5em;
  left: 50%;
  -webkit-transition: all 180ms ease-out;
  -moz-transition: all 180ms ease-out;
  -o-transition: all 180ms ease-out;
  transition: all 180ms ease-out;
}
.activetick:after {
  background-color: #a8d8f8;
  -webkit-box-shadow: 0 0 0.1em 0.04em #79c3f4;
  -moz-box-shadow: 0 0 0.1em 0.04em #79c3f4;
  box-shadow: 0 0 0.1em 0.04em #79c3f4;
  -webkit-transition: all 50ms ease-in;
  -moz-transition: all 50ms ease-in;
  -o-transition: all 50ms ease-in;
  transition: all 50ms ease-in;
}
.tick:nth-child(1) {
  -webkit-transform: rotate(-135deg);
  -moz-transform: rotate(-135deg);
  -o-transform: rotate(-135deg);
  -ms-transform: rotate(-135deg);
  transform: rotate(-135deg);
}
.tick:nth-child(2) {
  -webkit-transform: rotate(-125deg);
  -moz-transform: rotate(-125deg);
  -o-transform: rotate(-125deg);
  -ms-transform: rotate(-125deg);
  transform: rotate(-125deg);
}
.tick:nth-child(3) {
  -webkit-transform: rotate(-115deg);
  -moz-transform: rotate(-115deg);
  -o-transform: rotate(-115deg);
  -ms-transform: rotate(-115deg);
  transform: rotate(-115deg);
}
.tick:nth-child(4) {
  -webkit-transform: rotate(-105deg);
  -moz-transform: rotate(-105deg);
  -o-transform: rotate(-105deg);
  -ms-transform: rotate(-105deg);
  transform: rotate(-105deg);
}
.tick:nth-child(5) {
  -webkit-transform: rotate(-95deg);
  -moz-transform: rotate(-95deg);
  -o-transform: rotate(-95deg);
  -ms-transform: rotate(-95deg);
  transform: rotate(-95deg);
}
.tick:nth-child(6) {
  -webkit-transform: rotate(-85deg);
  -moz-transform: rotate(-85deg);
  -o-transform: rotate(-85deg);
  -ms-transform: rotate(-85deg);
  transform: rotate(-85deg);
}
.tick:nth-child(7) {
  -webkit-transform: rotate(-75deg);
  -moz-transform: rotate(-75deg);
  -o-transform: rotate(-75deg);
  -ms-transform: rotate(-75deg);
  transform: rotate(-75deg);
}
.tick:nth-child(8) {
  -webkit-transform: rotate(-65deg);
  -moz-transform: rotate(-65deg);
  -o-transform: rotate(-65deg);
  -ms-transform: rotate(-65deg);
  transform: rotate(-65deg);
}
.tick:nth-child(9) {
  -webkit-transform: rotate(-55deg);
  -moz-transform: rotate(-55deg);
  -o-transform: rotate(-55deg);
  -ms-transform: rotate(-55deg);
  transform: rotate(-55deg);
}
.tick:nth-child(10) {
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  transform: rotate(-45deg);
}
.tick:nth-child(11) {
  -webkit-transform: rotate(-35deg);
  -moz-transform: rotate(-35deg);
  -o-transform: rotate(-35deg);
  -ms-transform: rotate(-35deg);
  transform: rotate(-35deg);
}
.tick:nth-child(12) {
  -webkit-transform: rotate(-25deg);
  -moz-transform: rotate(-25deg);
  -o-transform: rotate(-25deg);
  -ms-transform: rotate(-25deg);
  transform: rotate(-25deg);
}
.tick:nth-child(13) {
  -webkit-transform: rotate(-15deg);
  -moz-transform: rotate(-15deg);
  -o-transform: rotate(-15deg);
  -ms-transform: rotate(-15deg);
  transform: rotate(-15deg);
}
.tick:nth-child(14) {
  -webkit-transform: rotate(-5deg);
  -moz-transform: rotate(-5deg);
  -o-transform: rotate(-5deg);
  -ms-transform: rotate(-5deg);
  transform: rotate(-5deg);
}
.tick:nth-child(15) {
  -webkit-transform: rotate(5deg);
  -moz-transform: rotate(5deg);
  -o-transform: rotate(5deg);
  -ms-transform: rotate(5deg);
  transform: rotate(5deg);
}
.tick:nth-child(16) {
  -webkit-transform: rotate(15deg);
  -moz-transform: rotate(15deg);
  -o-transform: rotate(15deg);
  -ms-transform: rotate(15deg);
  transform: rotate(15deg);
}
.tick:nth-child(17) {
  -webkit-transform: rotate(25deg);
  -moz-transform: rotate(25deg);
  -o-transform: rotate(25deg);
  -ms-transform: rotate(25deg);
  transform: rotate(25deg);
}
.tick:nth-child(18) {
  -webkit-transform: rotate(35deg);
  -moz-transform: rotate(35deg);
  -o-transform: rotate(35deg);
  -ms-transform: rotate(35deg);
  transform: rotate(35deg);
}
.tick:nth-child(19) {
  -webkit-transform: rotate(45deg);
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}
.tick:nth-child(20) {
  -webkit-transform: rotate(55deg);
  -moz-transform: rotate(55deg);
  -o-transform: rotate(55deg);
  -ms-transform: rotate(55deg);
  transform: rotate(55deg);
}
.tick:nth-child(21) {
  -webkit-transform: rotate(65deg);
  -moz-transform: rotate(65deg);
  -o-transform: rotate(65deg);
  -ms-transform: rotate(65deg);
  transform: rotate(65deg);
}
.tick:nth-child(22) {
  -webkit-transform: rotate(75deg);
  -moz-transform: rotate(75deg);
  -o-transform: rotate(75deg);
  -ms-transform: rotate(75deg);
  transform: rotate(75deg);
}
.tick:nth-child(19) {
  -webkit-transform: rotate(45deg);
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}
.tick:nth-child(20) {
  -webkit-transform: rotate(55deg);
  -moz-transform: rotate(55deg);
  -o-transform: rotate(55deg);
  -ms-transform: rotate(55deg);
  transform: rotate(55deg);
}
.tick:nth-child(21) {
  -webkit-transform: rotate(65deg);
  -moz-transform: rotate(65deg);
  -o-transform: rotate(65deg);
  -ms-transform: rotate(65deg);
  transform: rotate(65deg);
}
.tick:nth-child(22) {
  -webkit-transform: rotate(75deg);
  -moz-transform: rotate(75deg);
  -o-transform: rotate(75deg);
  -ms-transform: rotate(75deg);
  transform: rotate(75deg);
}
.tick:nth-child(23) {
  -webkit-transform: rotate(85deg);
  -moz-transform: rotate(85deg);
  -o-transform: rotate(85deg);
  -ms-transform: rotate(85deg);
  transform: rotate(85deg);
}
.tick:nth-child(24) {
  -webkit-transform: rotate(95deg);
  -moz-transform: rotate(95deg);
  -o-transform: rotate(95deg);
  -ms-transform: rotate(95deg);
  transform: rotate(95deg);
}
.tick:nth-child(25) {
  -webkit-transform: rotate(105deg);
  -moz-transform: rotate(105deg);
  -o-transform: rotate(105deg);
  -ms-transform: rotate(105deg);
  transform: rotate(105deg);
}
.tick:nth-child(26) {
  -webkit-transform: rotate(115deg);
  -moz-transform: rotate(115deg);
  -o-transform: rotate(115deg);
  -ms-transform: rotate(115deg);
  transform: rotate(115deg);
}
.tick:nth-child(27) {
  -webkit-transform: rotate(125deg);
  -moz-transform: rotate(125deg);
  -o-transform: rotate(125deg);
  -ms-transform: rotate(125deg);
  transform: rotate(125deg);
}
.tick:nth-child(28) {
  -webkit-transform: rotate(135deg);
  -moz-transform: rotate(135deg);
  -o-transform: rotate(135deg);
  -ms-transform: rotate(135deg);
  transform: rotate(135deg);
}

.knob {
  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAgAElEQVR4nMVdeUAWVdf/NY7j4zAim2ia+YqiuGJuFCm4gyFqromiaInkS7igoFgKpamoiKiFCwgEKIpauaKgCC5gLpniirmQS+4LbtCr3x80l9lnHqC+31/wzMy955x77nbuOeeiX79+1L179xio4P3336fVnvGoWbMmvWfPHg4AMjMzWaV3Fi1aRG3cuFG1HqOwtbVlN27caAkADx8+pPPy8uyk7zx69EhWz44dO8h7qampTN++fQmdPF3R0dF0bGwsV1kaeURHR3NOTk4m/v+BAwdq8j9w4EAOt2/fJi95e3vrCp+Hs7OzouArg6KiIkr6W3h4uL3edzY2Nibh/0ePHjWpvcsjICDA1LBhQ00eHj58SJ7/+OOPRE5ubm6q31lYWHCXL1+uskaVgWVZZv/+/dSBAwcMN9bKlSvNaqyoqCjVsp8/f/7PMfc3GjRooKm5oaGhouebNm3ipk6dSgOAk5MTof3UqVMiPsLDw9nc3Fyuc+fOujx06tRJpowiODs7MwMGDBANB6WlpSZXV1f6zz//VKzA0dFRVzNLS0urvGcFBwdzHTp0UGTI3t5e1tjFxcWKNNSvX19bKBrgOI7bvn07BQBLliwxrETNmze3AoAvvvjCVFhYWFb/rVu3uKSkJJEwN2/ezAB/j2sqWLduHXnm5eUlY8bb25swfu3aNaJlL1680G04Hu7u7kx+fr6moPLy8kwAMGLECFG5HMeZAMDT01O3d7u7u1sCQG5uLtW6dWvNHtOuXTtRPatWrRI1cI0aNcj3o0ePNvHzqx569Ogh5jMiIkI0Xnt7e8smTCkOHTpEmO3bty8pkKIoytbWlvy/du1aVSYDAgKY3377jbx78OBBmQbHxMTIhDpgwAAimK1bt8qeOzo6mkaMGCFrzK+//lpEy19//UUBwNWrVyvUe+fOncsFBATYS4fqDRs2cCaTSdQYWVlZ+nVUr16dMPbw4UPG09PT8Gro/v377MmTJ00AcOXKFVKZo6OjTEAWFhbcV199xcTFxVVq2PL29uZmzJhh9vDy6aefioRTUFBgiI6cnBwinw4dOtDp6emqPa5z587slClTWAAIDAxkPDw8yLsZGRmG5+EqRdOmTWkAuH//vuGhSQhHR0eRoAYPHkzKOXXqFJuSkiIrNzQ01M7e3r5C9QEAGb9VIG1MACgpKVFtUGlvc3Z2VqQtMjJSXO6GDRvo6dOnywpOSkqiJk6cWOFJzlx8+OGHFAB07dqV0PLs2TOZELy8vLjOnTtbAcDVq1dJT163bh29YcMGxZ595MgRIowWLVoY6v0///yzSICtWrVSFOiWLVtE5QUGBsree/Hiha4ct2/fXvYdPyG+fv2aSktL0/xQODErgV9/P3nyxKyuuW3bNpngQ0NDScP4+vqSvxcvXmzWMrhLly4mQLyPAIC0tDRF7eY3lfxS+PLlywwA3L17l6ldu7Zhvp4+farae7Zu3SqT89tvv22Zk5NjqfhBQECACQC6d+8uau2lS5cSYZw6dUpRMO7u7pXajXfq1KlC42y9evVE3x06dEhz+PrPf/4jeu7h4aEoQGtra/J7fHy87pA4atQoCgDmz5/PeXt76ypP//796aKiogoPtYiPj2d5rbt7926FhC/dyX755ZdWAPDJJ58oljdmzBhVbevWrZvis//+97+atB07dowFyhYxSs/5IVSK169fc8nJydTixYt1hZiTk0P4/PXXX2WNc+3aNeURKSkpiRsxYgRZ8jZv3pwuLCw0dezYkXwg1KCJEyeatUqKi4vTHUNv3LhBFRcXi7T86tWrhoencePG1TOHJiGeP39OGsXJyUm1ziVLltQ7ffq0YSWMi4tT7e0ODg4MADx8+FAsm9jYWM0KmjVrpinMgQMHEk2ZOHGiTGtatmxJAUCbNm0UiSsqKhIJQGgYHDZsGCnv8OHD5HuKojS188GDB0RhevfuTQHA7NmzyfcnTpwgf+tZDnr16iWri593jcLCwkKR94CAAOXGb9u2baWtsABw4MABUkFpaSlpyKlTp4qYVlq2AoCPjw8HAO3bt5c9T0pK0lSM48ePa/Ig1fx58+ZRvr6+sjL1FHDevHmmrl270sL/+b/v379vWI5jxoxRrmfVqlVkN/7o0SNNYnQNYH9j2bJlhOD33nvPEJEzZsxgAeDZs2cVVo74+HhV+mrVqqX4LD093cqcOpydnVmWZXVpfPTokUgJjxw5UjEjqdIGSIgOHTowAHDv3j160qRJ9YuKioTawgHA7t27WQAYMGBAle1jPD09iSZWq1aNlCs8Mjh69KhIUA4ODqq8rFixggKAyZMnmyWo/Px88n5YWJgVAOTl5ek2UGRkJD179mwOAK5duyar09PTk/rqq6/KGrFRo0YUINZsIcaPHy/63cHBQTbuHjp0SPTbsGHDKH41Zi6Cg4Op5cuXixqzZ8+emmO9m5ubYuPn5ub+6+aKKVOm0Pn5+dS9e/cU6xZuaAHg+vXr5bz9/PPPMkaXL1/O1apViwPKxlr+93HjxpnF3PPnz8n7u3btslF7z8/Pj+vZsye9aNEiU69evWT0zJs3j46MjLQ5f/68iJGQkBAaAIqLi+lOnTpV2qwfEBBAeE1PT+f4BY+lpSXLT8wsy1J/vyvTcqnVV4iMjAxV5Zw8ebLys8jISLZNmza6XXjixImGGyYzM5Py9fWt0Pi5adMmWT0ZGRkVPrD64YcfDH3bvHlz5R0zgHbt2sloysvLMzw0K1klVPH555+LCt64caMhrfvtt990K9m3b5/m8CW0Amhh9erVdjNmzDAtWLCAqlevHmVpackAwM6dO2XfBwQEqI7tISEhVXISefPmTdM/emTLw8LCglHa0K1bt45u2LAhBQAhISG6mvH7778zANC4cWOiWWPGjNGdBIUbUaFdywgKCgpUNVwJy5YtU1SWxo0bawp63759is+fPn3KAEBJSQn94sUL0/r163XpiYuL41auXCkuj9c2Pbi5uVFjxoxhfvjhh0rvX4SbNB7Z2dnClRvdq1cvWcPv379ftZFq1aqlSpe/v79VjRo1KqzR9evXZwDxGQkAnD17VldphOfvUqgaLpcuXWoJAOPHj1et4MMPP2QBYM6cOaJC+FXamTNnNOeYnTt3sn5+fqLTtBo1apgaNWqky1Tbtm1F71y4cIGuXbu26ndpaWkyWv73v/8RYX733Xeib6dNm0be3717t6Ge1qZNG1OzZs0YAOjbt6+qMkRGRqrSyTBMOZ05OTl2/NCiBB8fHxFh/OpGisDAQE2BPn/+3PDk5+PjQ+p49eqV4pDSq1cv6sWLF7I6eVtbixYtVBWjZs2ahJZ169YRO15ycjKnZppXwsiRI2neCnzy5EndEePp06cymmbPnm1SPeI+f/68IvPdu3cnH8yZM0fWQyZPnkwYHD9+vO7ut2XLluzChQt1fa5mzZplL10WDhgwQDbkODo6GhqGhPNX+/btRYJXWrZGREQoCurx48eqjV1SUiL6xtPTk3ZwcCAycXNzM29/JlzWMgxDBQcHc9WrV5dpt8lk4gYPHkwDwLJlywwJxN/fX7ivMYWEhNBdunQRlV2zZk02MDCQKi4urvg5gQQXLlxQ7Z3nzp2z2r17t0iIX375pahxjh07RmipXr26ag/q3Llz5WnesGEDEaZU8CtWrHhH+H9xcbHwOal87NixJgC4dOkSacxNmzbJhPDjjz8qata2bdvMYuTOnTsUALRv315zvurSpYvmMLJmzRryfNq0aeRvV1dXQnvfvn1lytamTRvVRqEo6p+3Dty5c4eNiopS3W2rYcGCBZSW68uoUaNoQOyTFB4eThjy8PAgv798+ZIFxJtD3lLdv39/mdDeeust0W92dnZM8+bNydFs+/btq8TKbRRJSUkVq+/GjRuEkQkTJii2du/evUWFK7n96OHZs2eiHiQ0kScmJpJnLi4uunNSYWEhO3fuXBYob+TBgweLGoR3qs7IyGCEh1KVBX+iOXPmTJnCUhRlsrOzo1xcXJgJEyaw06dPVx0JyL5n1apVhoeLtLQ0DgAYhjEBwKeffqr5bWlpqSrjCxcu1Fx1Cc8dpHj8+LGo3Fq1asl64YULF0S09e3b12748OFWb968kb27YsUKytXVlT1x4oQVTdMMID8Z7dOnj+h/Jycn7ty5c6SOuLg4et68eQwACG1rt2/fNk9Zv/jiC7ZOnTqKwhk8eLBhTRoxYoSo4v79+xsmxMnJSXFYU/LNVYKFhQURjNDe9OLFC9JLvv32W5nyDBs2zPASV+jTXFpaanj4piiKES6zK4R69erpEWqWOaOoqIgFgO+//97sXfLevXtF3yQmJlZ6JcNxnGXz5s3tgDJrrtI7T548MVyPp6enYhk//PBDxRti9+7dlTKSLVy4UERUdna27k43NDS0nqurq0m0U/2X8d5771EAcO7cOU3hWVpa6tKYnJxM9laFhYWkQR88eEADwNtvv22eMml5XfDQWmo6OztXuWCVPBi3bNlS5fUsX76c+/jjjw0N0e+++65IsEJzjBHwm2shWJZVH3W2bdsmIozfAALAjh07aB8fH6spU6Yw2dnZTKdOnUwAkJKSQgR35swZWeG8E7IWlM4ssrKyNJWEDzuQIjc3V/G7w4cPE96koQoODg5sbm4uExQUxMbFxVkCyhFTRs5A+KPs8PBw0bvHjx+nnjx5Yt5o9O677xr6wMnJSZMwnqj8/HyydI2JiSECvHPnDpeXl0fqGjBgAMUwjExLL126ZNZYvGDBAmbChAn8iZ9qb1IzYwgdvn/66SdRgwwcOFCVFg8PD7N6yqtXrxgfH5/y8pXi+qKiomjpsjI1NVXV7rR8+XJDRPTs2VNxOJCGJ0gFoIY9e/aIyrO2tqYaNmxoun//vmIDWFtbm/g9SlZWFnlHSQZGcPDgQbMXFydPnjSvrnPnzpmGDh1KAYCtrS2t50gnRExMDAcAJSUlipUGBwfLGHj16lWVh7gVFBTINpK8r6+DgwOhTeqAzePXX3/V3Ih+/fXXivxxHFd189rp06dZDw8P1YipW7duyYTp5uZWqVVZy5YtmdTUVFJG586dGaDcOULPDjV27FhdbRMOSSNGjGDWr19vAoB79+7J+BHGoUyaNEnEG3+C+ccff9BCWqsC27ZtYwEgOjq6TP4zZswQNUTDhg01u2JMTIymIGbMmEGlpqbqav5HH31EAYCVlVWl9xUdO3Yk9aWlpVW5jWrjxo1mDTX9+vUzpKy9evUi78ncbb/66ivRviE1NZW5ffu2IiHnz58XfbxixQpScP369Wk7OzvZd9K5on///oqNNmDAgCrr+lI6eYSGhpoA4PLly/aC30RC3LRpEwMAV69eVZTBsGHDOCXnCh4hISHMoEGDKAA4efIkK+yBQqidzYsg1Dg99OvXjy4tLWX4zY8ahL1Gar52dnZmee/EZs2asQDw448/EkJ37dpFtF6YhUGKrl27am5GP/vsM0Xh/v7777r8Pn/+XLUn79ixQ8S71N0nIiJCt4dJY1wIVq9eXaEu3759e1mlbdu2NWs44s3jfIaJPXv2yASl53YkPNdQw8iRI7k5c+bYAwAftKoFKysrVWUbM2aMbBHQrFkz1TKlRk9V9O/fnzDC5+XIzMw0hYeHE0NaVlYWKezMmTOqrZ6WlkbeU8o9wkNoFAQAqSsMH06gBqUY8EOHDokMf15eXroN1K1bN1E5LVq0UKx3165dhoQ5btw48p7eGX1CQoKYvgkTJhiasJTcIW/cuEEB8j3BsmXLTMIzkydPnjAA8NdffzEjR47Uq09Wz+7du+3Onz9veFX35ZdfkjImTJjAAcDx48dF39erV88E6NuwpPDy8uICAgJEPaZRo0YVGlUUfduEk82+fftMPj4+DFA2aVWkEh61a9cWCZb3Ev/1119FRMyfP1/KnOj/n376qcrtVgkJCYZ5++abb1gAaNCggRVQ3vuvXLmiWcaUKVN0G9rCwoL0ZpJTRWos9PLyYgMCAhS7mbu7uwkAatSooSsktcAcKe7evSuq68CBA0Tb6tSpozvZLliwQJPxuLg4RTr0lvc8TCaT2cvylJQUBgCioqKsAPXNsiYsLS0ZqQv9oEGDDBEzd+5c1S67du1aYWwHq3botXXrVkN1FRYWsm+//XalDnzc3d1ZoGyFqPXe9OnTWS1N9/Pzk/Hy008/cQAwZ84cB39/f02FMhyvefnyZaGthwhq1KhRikJ78+YNIdrX15fZuHGjIqM0TVOAPOCex+bNmykASEhIYAsKClQbqGfPniYAePXqFbdu3TorAMjOzub439Q5A7y8vES0LV261KQUHwkA9evXZ0tKSkwAkJOTQ2dnZxM+u3TpotqYp06dEjViaGio4nKc58MsPH36lALKAmmMvN+4cWNRqwcHB7OCvxXLmDBhggko60F65bdv3545fPiw7L1x48YpNrIwZvHcuXOid2bPnm0JAI8fP5aV16FDB7PnUHd3d2rmzJmGJnjhVMGyrHpdlpaWiq1WXFzMOjs72wtPFpcsWSLSkg8++EC0Jl+7di15HhQURJ84cYIDgO7du8sI6NOnj6HJe8iQIUR4bm5uMuZZlqUBYMGCBZzQ54xHRZKiJScnixRJmn3IxsamasL3+B2kr6+v4WWbs7OzauUhISEsYNwkL8SlS5f+8TiLP//8kwaAgoICw3VNmTKFGz58OOFn8uTJqrLiI8/atGlTcXva0KFDVT92dXUl2si7+Rs5r1i7di27c+dOs0zrTZs25T7//HNVQfGTJQDUrVtX97z+448/ZoHyE0UjG0QhcnJyKACYPn06DQAURVWJwuzatYsFgHfeeUdbaW1sbLjVq1ezQFkoWnBwMOmWa9as4SwtLUU9Q8+D5ObNmyYAyMjIEH5HS4+HpdDK3snnYQGApUuXsgAwevRo0vAzZsxgAKBmzZqENuEJJO8vfOvWLVXa+WQHajCy5OfRtGlTDgA6duxoUgtns7CwYADJgunq1atE44YNG0YBQO3atQ1p1L59+2gACA0NVSW0U6dOplGjRulqWIsWLVgA6NOnD2dvb68VlEPKql27tkiAb731FmFs1qxZJgBITEwU9ajRo0er+lX98ssvIr6FMSQ9evTQlMnSpUtNAHTnEz7Ghke1atXKym3durVijpCkpCRN4SUnJxvqvnZ2dqKKeW1QQ35+foXGXn4jJoS/v7/qgVudOnUUh4srV65U6mzG1dWVKGVCQgL1ySefyOSUnJyszaOWkVCKly9fUkC543D37t0VtViYD/jYsWM2APD06VPujz/+UGzIadOmUXyyFjV/4qqC0cMjHpGRkYYaqV27diZ/f3+mZ8+eTFhYGAsAK1asEPVMoVO5MPB0z549VRZ6QbBp0yZDk7i3t7fahGxIUJmZmaoaxlsWZs+ercqgcOHg6upqSBAnT55khIdwdevW5f6uz6pp06ZEyCtXrjS7h6enp5fTMGjQoAppo6BFqcePH+v2sE6dOvHmfEbqraEVjaSH6OhowwKws7OjAeD8+fPML7/8YpZGbt68mSib1D2Un3O1QNM0GxoaysTHx5N92t27d5X5fvDggYipNm3aGBrCJk6caEij1bJ/CqNtpdi7dy8LlGnzzZs3qVatWlEkL6EA3377LSPMGKEEe3t7xUa7f/++jP7du3fTQJnHTZMmTUxjxoxhhck89fYv7dq10x0leOu14iKIzzUbHh7OHDt2rEKa+vTpU/qzzz5TOigSCeKLL75ghUmG1eDg4CAa0oS5sp49e8YCQHx8PCc9g7hz546iMM6cOVNpp4ewsDDNHiVMGMofPUt5/eWXX2QrO2nSNhGaNm1aoYll1qxZXGxsLCn4yJEjIsH4+/ubAGDZsmWqPW/s2LGKmifV4oULF1qmp6fr9mBNRgG8fv2aGT16NAWURfPyv5uzx9DD1KlTZXSqRTATqHllAOUhBEKMHz++wrtV/mqJIUOGqDb82bNnuXXr1hHNiouLU9Xu7777rlLC09qgWltbc7du3WLUopKN4MaNGywArFmzxgSoZ9VTxWeffaZaeXR0tKo3n1paJyn0YiVOnz7N3rx5kwYArU2hEaSmptLCVH9VgYMHD1J79uwx24g4bdo0VSX28vJSp7F69epsREQE/fDhQ9UC+ET6Tk5O1Llz5xQLMzJPAEBWVpah9968eVPla3ShE4YUPXr0oF+9ekXPnz9fkT8XFxdD0VMrVqyQ1dG2bVtV2WZnZ4vfVzr9AsQCzsrK4jiOI4S6uLio9g4bGxtDPYc3b/CQpvV49eoV27p1a7p3796Gh8uIiAhu4sSJmg0eHh5uAoxbfqWrUaA8fxYAXL9+nQPKzla6detGeJfaAAH9RYIm1HyrOnfuTLz+Hj58SAjgfW4TEhJEhCQlJdGAsesjeLz11ls0AAwaNEimrVpXafj5+bHDhw8XPZcG2fBYsGCBrGw1C/jp06d1Bfn8+XPVYai4uFhVSdTMOQSJiYkihnJzc0UfKJ1f8LvOwMBABgCCgoIslbLvfPPNNzYAkJGRwTo5ObGvX7/mDh06xAFAu3btOGE67t69e1OHDh2iACAvL0/GbFhYmKaGN2nSRPQ8JSVFNB8Kg5GUIHUxFeL333+Xaf/3339PaNy5c6dIZlqppi5fvlxeFm/Zzc7O1pwIHR0dSQsPHTpUxsjUqVMJ8f369TNr/b9+/XrDE2bbtm0tASAxMVFUR+vWrSnhXSSA2FQiBH+yKIQw7SsAVKtWjRsyZAi9d+9eRUNlx44dLQFxrmAlCJNn6mLOnDkywc2dO9cEGJ8HeAitneZAmupJCN7sUlHw96GMGzdOcTK+fv264lAxadIkqylTpgg3peTcgk8c+sEHHxBB9+rVi+3Tp4/ZtDo7O4u/4S2TSrC2tqZdXFwUCeY3VlIo3WojxPz58xnAuFumElauXElnZWWpnoMIYTQ8T4jly5cbWjLzCRSEePnyJfvmzZt/L6pYz81GiL179zJAeaALUJ7Ia8uWLYrl2NnZKQr2xIkTZu0rhHdkffDBB7JvX79+TTTT399fVbNfvnyp+EwpNn3kyJEyS/bIkSMJP0pZJEQQmjP4rGhbtmxR1XA+xR0AXLlyxdCYbzTUa9u2barljRs3jgOAgoICs4aEK1euMEBZvnYPDw+ze0ppaamhb6QXkv2rUNLsiIgIE2+76devn6YDgjRniBYuXbrExMTEiN7/6KOPOD4+MDQ0lAL0L5sBgPz8fLZu3bqaSsT7HX/44YeVcmjgL97k/QqE6NKli1LZxmTyzjvvaDLAe5brwVxTiHRVIrzC1Ai8vb1ldOvdkCYMEKos7OzsqI8++sgEyH2Ppelrr1+/br5PF5+/UM0FlE+NpARhljXe0UF43Z5RCK/JMwd6ztLHjh1TtVAEBQXJvtXK5cjj559/pgEgMDCQBoBFixbpRZfZDx061JjS8tZXb29vQ+O3cC+iBE9PT11N7Nq1q2JdwiuRhg8fzh48eFDE6JkzZ/6xsbxbt26qZUdFRcmeBQYGGupxffr0MQHikD9duLi4KHYrYax3q1atFAsUXo3EXwh84MAB1cqfPXvGNmjQQPQ8LCzMVFhYSBgsKSlR1DjecxIoDyp1dnY2SRcgdnZ2hKZHjx5Veok6evRoprCwUMbT4sWLWaUUU1euXGGENxjJcPToUWbmzJmaLXrt2rUKEb569WpamPwSKEuvKn1Py1Cphbt375oAQMnlRgnW1tYyQfCJ2QDAzc1NkQ5phjoj8PX1/XdWX/xtZEbh5+dHA/IrWMPCwkg5TZo0EQlCGoImBG/wnD9/foXvnuIRGRlp1lLaxsZG8f3s7GzVcq5fv04vWrRI9lwYp24YLi4uooL4TVReXp7p8ePHhjQgKChIpnUVvekgNjZWpAxCHzBzNq0AEBYWptgb+DzE27dv1yxvw4YNhnu1g4MDxZukpBA5lgQFBXGA+m0Ias4DeuDHeSUn5YSEBBlh0riS5ORkVWb5YJnDhw9XekgQnmlooUuXLmbJQXpP+/fff88AZRc3A+JkC3//X/Z+cHAws3XrVsrDw4NLT09X7HatWrX6x0MFtLB+/XrNYaWoqIgbMmSIqplddIuNBEIPQqVU4FqwtbUl78fGxirKaPXq1RxQnhtGOFf6+flRs2bNKleIzMxMJjc3l/wQFBQksoguWbLEEij3GudhY2Pzj05Wtra2/68KIEVqaqpVfHw8l5eXp9lgGzdutJPmgOe9KNW8KT09PSkAaNq0qVjppJcUHz58mMnNzVV1bpBm4+FXFHXq1CHC3LFjh0yzpTcz68ZJSCDN0R4QEKB4VpGfn1/hqKbt27dzUtsXvxRPSEgg9c+cOdNwHUrWAxk2b95MKhVevihFx44dK3UmwacBNBerVq1iAKBOnTqEthMnThDG+PAFHrNnz2YAgGEYFgBiYmJ0E/4DgLu7u4h3YfyIWsZRI7h48WLV+XwNHDiQkXpCGLm4BADef/99kTZEREQQLd63b5+ipoSGhlIjR44kglA60ePRsmVLkfbyVl2g7FhY8ozUN3bsWLMUa+3atYpDp1JKD6AspWF8fLym4PnsFzz2799fseG/ZcuWnNCeNGrUKEPMFRUVUZMmTdJ9Nycnx/T555/TsbGxXExMjOpQOW3aNJPaRZFKSElJMUvDz549a2j+un37tmK50nxdiYmJrPRY+c2bN1xmZiZpOBcXF5u7d++KeXr58qVul7p48aKM2DVr1si+4xNd9ujRgxE2hp+fn6Y2NG7cWLXhhJqXnp6uS6s0vyEfS//XX3+ROvgEBLyDhRRS/2Qp0tLSuIyMDDokJESYW8WsuWvJkiX0sGHDLJVyjCmipKREVcOklQtPBtWW0EIII1pTUlLs1ZL6q50iKkErU6pWQ1pbW1OhoaGsNNFaeHi48FCO+Zse0oBr1qwh9dna2rIA8Oeff1ZsGBLacIDyRDDCMGAAaAVaj5QAAALLSURBVNKkiW63/+abb1S7Op+k3lycPXvWBAAlJSWq4WlKUNrERUVFUQDw4sULUYNdvHhR1kjCmJWvv/5acfg8fvy4WbfBVQqDBg2SCfDRo0fM8OHDWX7Zd+TIEUVtMxIydvbsWRoou/rIKE3Cy5N593+liFn+PsbQ0FBRI+7fv19RKaZOnVrpcAVzwDAMO378ePXhid/sFBQU6I5hWv5FaWlpVZPNQAdqGasBICAggD58+LDicyP3CUohzJKXmJioqjzTp09XrNNoAgEjIRYE/OUqHh4eZmuSr68vOcrkcfHiRZO1tbUJAFauXEm0mD9lk+L48eM0UH53IL80NmdTZg7mzJnDAeUTfmhoKFNUVER4p2n633NoOHLkiGZlf/zxB62Ww116arZy5UqO95WiaZpo0MuXLzkAaNCgAflNLQGk9AJHo6AoSvW7J0+e0Hz0MH8He6NGjUjvEd45wqNFixYcfwNOtWrVZLTWq1dPphzR0dEsULbPELrdOjo6qplQjPHKZwS1tbU1AWW3qBn6EICPjw8hZOfOnVRwcLCsl/HJ6s118VECx3Gqw5k0ZZRapjo+ZsPe3p4IWXhaqYS+ffuy5twVMm/ePHbXrl2ULM4yKipKJISUlBQ6NjaW4TPuqDkACDF48GBDhKhFI5HUdhWEWk6Vli1bmj1nCG+Zk0Lt1uv79+8bop/PnaKGunXrlpUjzIdev359GXN8Wj8AOHXqlKHe8eDBAw4oiyc5fvy4LsEff/yxMNJVtesmJiZyDx48qNAwVpnway3wi5kbN24wBQUFNkB5ggUt9O7dm2ndujUjuxdReG13dHS0rKCjR48yfCz28OHDGaD8gnclt6DmzZvLynj27Bl94cKFKgsxe++994i2ZmZmajaQWgOqXYaWl5dH169fnwOAqVOnkndOnz5NeOXzfgmhdy2e0h1YALB48WKGz6/yf8RxFhxL0FjRAAAAAElFTkSuQmCC);
}

  
  
  
  
</style>
