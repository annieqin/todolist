var myApp = angular.module('todolist', ['ngRoute', 'ui.bootstrap', 'angularSpectrumColorpicker', 'xeditable', 'ui.timepicker']);

myApp.service('getCateTemplate', function($http, $q) {
  return {
    getHTML: function() {
      var defer = $q.defer();
      $http.get('/static/js/monthCategory.html', {cache: true}).success(function(response){
        defer.resolve(response)
      });
      return defer.promise
    }
  }
});

myApp.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

myApp.controller('TaskCtrl', function ($scope, $modal, $http) {
  $scope.popup = {
    opened: false
  };
  $scope.open = function() {
    $scope.popup.opened = true;
  };
  $scope.$watch('date', function(newValue, oldValue) {
    if ($scope.date != 'undefined' && newValue != oldValue) {
      window.open(
          '/?selected_date=' + $scope.date.getTime(),
          '_self');
    }
  });

  $scope.showCategoryCreateModal = function (level) {
    $scope.category = {
      content: '',
      color: '',
      level: level
    };

    var categoryModalInstance = $modal.open({
      templateUrl: 'createCategory.html',
      controller: 'CategoryModalInstanceCtrl',
      resolve: {
        category: function() {
          return $scope.category
        }
      }
    });

    categoryModalInstance.result.then(function (result) {
      $scope.category.content = result.content;
      $scope.category.color = result.color;
      $scope.category.level = result.level;
      $scope.category.newMonthCate = result.newMonthCate;
      $scope.category.newWeekCate = result.newWeekCate;
      $scope.category.newCommCate  = result.newCommCate;
      //$scope.category.id = result.id;
    });
  };

  $scope.showTaskCreateModal = function (category_id, category_content, level) {
    $scope.task = {
      category_id: category_id,
      category_content: category_content,
      level: level,
      year: $('.current_year').val(),
      month: $('.current_month').val(),
      week: $('.current_week').val(),
      day: $('.current_day').val(),
      weekday: $('.current_weekday').val()
    };

    if (level == 1) {
      var monthtaskModalInstance = $modal.open({
        templateUrl: 'monthtaskCreate.html',
        controller: 'MonthtaskModalInstanceCtrl',
        resolve: {
          task: function() {
            return $scope.task
          },
          monthtasks: function() {
            return $scope.monthtasks
          }
        }
      });

      monthtaskModalInstance.result.then(function (result) {
        $scope.task.content = result.content;
        $scope.task.visible_range = result.visible_range;
        $scope.task.monthtask = result.monthtask
      });
    }

    if (level == 2) {
      var weektaskModalInstance = $modal.open({
        templateUrl: 'monthtaskCreate.html',
        controller: 'WeektaskModalInstanceCtrl',
        resolve: {
          task: function() {
            return $scope.task
          },
          weektasks: function() {
            return $scope.weektasks
          }
        }
      });

      weektaskModalInstance.result.then(function (result) {
        $scope.task.content = result.content;
        $scope.task.visible_range = result.visible_range;
        $scope.task.weektask = result.weektask
      });
    }

    if (level == 3) {
      var commtaskModalInstance = $modal.open({
        templateUrl: 'commtaskCreate.html',
        controller: 'CommtaskModalInstance',
        resolve: {
          task: function() {
            return $scope.task
          },
          commtasks: function() {
            return $scope.commtasks
          }
        }
      });

      commtaskModalInstance.result.then(function(result) {
        $scope.task = result;
      });
    }

    if (level == 4) {
      var temptaskModalInstance = $modal.open({
        templateUrl: 'temptaskCreate.html',
        controller: 'TemptaskModalInstance',
        resolve: {
          task: function() {
            return $scope.task
          },
          temptasks: function() {
            return $scope.temptasks
          }
        }
      });

      temptaskModalInstance.result.then(function(result) {
        $scope.task = result;
      })
    }
  };

  $scope.taskdone = function(task_id, type) {
    $http.post('/taskdone', {
      'task_id': task_id,
      'type': type,
      'status': $scope['confirmed'][type+task_id],
      'year': $('.current_year').val(),
      'month': $('.current_month').val(),
      'day': $('.current_day').val()
    })
  };

  $scope.commtasks = commtasks;
  $scope.temptasks = temptasks;
  $scope.monthtasks = monthtasks;
  $scope.weektasks = weektasks;

  $scope.edit_task_content = function(data, type, id) {
    //$scope.commtasks[id].content =  data;
    return $http.post('/edit', {
      id: id,
      type: type,
      content: data
    })
  };

  $scope.delete_task = function(type, id) {
    $http.post('/delete', {
      type: type,
      id: id
    }).then(function() {
      $('.'+type+'task-'+id).remove()
    })
  }
});

myApp.controller('CategoryModalInstanceCtrl',  function($scope, $modalInstance, $http, $q, category, getCateTemplate) {
  $scope.ok = function () {
    $scope.category.level = category.level;

    //getCateTemplate.getHTML().then(function(response){
    //  $scope.category.newMonthCate = response;
    //});
    //$http.get('/static/js/monthCategory.html').then(function(response) {
    //  var monthCateTemplate = _.template(response.data);
    //
    //  $http.post('/create_category', {
    //    'content': $scope.category.content,
    //    'color': $scope.category.color,
    //    'level': $scope.category.level
    //  }).then(function(response) {
    //    //$scope.category.id =  response.data.id;
    //
    //    $scope.category.newMonthCate = monthCateTemplate(response.data);
    //
    //    $modalInstance.close($scope.category);
    //  });
    //});

    $http.get('/static/js/monthCategory.html').then(function(response) {
      var monthCateTemplate = _.template(response.data);
      $http.get('/static/js/weekCategory.html').then(function(response) {
        var weekCateTemplate = _.template(response.data);
        $http.get('/static/js/commCategory.html').then(function(response) {
          var commCateTemplate = _.template(response.data);
          $http.post('/create_category', {
            'content': $scope.category.content,
            'color': $scope.category.color,
            'level': $scope.category.level
          }).then(function(response) {
            //$scope.category.id =  response.data.id;
            $scope.category.newMonthCate = monthCateTemplate(response.data);
            $scope.category.newWeekCate = weekCateTemplate(response.data);
            $scope.category.newCommCate = commCateTemplate(response.data);

            $modalInstance.close($scope.category);
          });
        });
      });
    });
  };
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

myApp.controller('MonthtaskModalInstanceCtrl', function($scope, $modalInstance, $http, task, monthtasks) {
  $scope.task = task;
  $scope.monthtasks = monthtasks;
  $scope.ok = function() {
    $http.get('/static/js/monthTask.html').then(function(response) {
      var monthtaskTemplate = _.template(response.data);

      $http.post('/create_monthtask', {
        'category_id': $scope.task.category_id,
        'content': $scope.task.content,
        'visible_range': $scope.task.visible_range,
        'year': $scope.task.year,
        'month': $scope.task.month
      }).then(function(response) {
        $scope.monthtasks[response.data.id] = response.data;
        $scope.task.monthtask = monthtaskTemplate(response.data);

        $modalInstance.close($scope.task);
      });
    });
  };
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

myApp.controller('WeektaskModalInstanceCtrl', function($scope, $modalInstance, $http, task, weektasks) {
  $scope.task = task;
  $scope.weektasks = weektasks;
  $scope.ok = function() {
    $http.get('/static/js/weekTask.html').then(function(response) {
      var weektaskTemplate = _.template(response.data);

      $http.post('/create_weektask', {
        'category_id': $scope.task.category_id,
        'content': $scope.task.content,
        'visible_range': $scope.task.visible_range,
        'year': $scope.task.year,
        'month': $scope.task.month,
        'week': $scope.task.week
      }).then(function(response) {
        $scope.weektasks[response.data.id] = response.data;
        $scope.task.weektask = weektaskTemplate(response.data);

        $modalInstance.close($scope.task);
      })
    })
  };
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

myApp.controller('CommtaskModalInstance', function($scope, $modalInstance, $http, $timeout, task, commtasks) {
  $scope.task = task;
  $scope.commtasks = commtasks;

  $scope.popup1 = {
    opened: false
  };
  $scope.popup2 = {
    opened: false
  };

  $scope.open1 = function() {
    $timeout(function() {
      $scope.popup1.opened = true;
    })
  };
  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };

  $scope.ok = function() {
    var frequency = [];
    angular.forEach($scope.task.frequency, function(value, key) {
      if (value==true) {
        frequency.push(key)
      }
    });
    $http.post('/create_commtask', {
      'category_id': $scope.task.category_id,
      'content': $scope.task.content,
      'visible_range': $scope.task.visible_range,
      'year': $scope.task.year,
      'month': $scope.task.month,
      'day': $scope.task.day,
      'weekday': $scope.task.weekday,
      'frequency': frequency,
      'scheduled_started_at': $scope.task.scheduled_started_at,
      'scheduled_finished_at': $scope.task.scheduled_finished_at,
      'started_date': $scope.task.started_date,
      'finished_date': $scope.task.finished_date
    }).then(function(response) {
      var data = response.data;

      $scope.commtasks[data.id] = data;

      if (response.data.show == true) {
        $http.get('/static/js/commTask.html').then(function(response) {
          var commtaskTemplate = _.template(response.data);
          $scope.task.commtask = commtaskTemplate(data);
        });
      }
      $modalInstance.close($scope.task)
    })
  };
  $scope.cancel = function() {
    $modalInstance.dismiss('cancel')
  }
});

myApp.controller('TemptaskModalInstance', function($scope, $modalInstance, $http, task, temptasks) {
  $scope.task = task;
  $scope.temptasks = temptasks;
  $scope.ok = function() {
    $http.get('/static/js/tempTask.html').then(function(response) {
      var temptaskTemplate = _.template(response.data);

      $http.post('/create_temptask', {
        'content': $scope.task.content,
        'visible_range': $scope.task.visible_range,
        'year': $scope.task.year,
        'month': $scope.task.month,
        'day': $scope.task.day,
        'scheduled_started_at': $scope.task.scheduled_started_at,
        'scheduled_finished_at': $scope.task.scheduled_finished_at
      }).then(function(response) {
        $scope.temptasks[response.data.id] = response.data;
        $scope.task.temptask = temptaskTemplate(response.data);

        $modalInstance.close($scope.task)
      })
    })
  };
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

myApp.directive('monthcate', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('category.newMonthCate', function(html) {
        if(!html) {
          return;
        }
        var content = $compile(html)(scope);
        content.insertBefore(elem);
        //elem[0].outerHTML = html;
        //elem.html(html);
        //$(html).insertBefore(elem);
        //$compile(elem.contents())(scope)
      });
    }
  }
});

myApp.directive('weekcate', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('category.newWeekCate', function(html) {
        if(!html) {
          return;
        }
        var content = $compile(html)(scope);
        content.insertBefore(elem);
        //elem[0].outerHTML = html;
        //elem.html(html);
        //$(html).insertBefore(elem);
        //$compile(elem.contents())(scope)
      });
    }
  }
});

myApp.directive('commcate', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('category.newCommCate', function(html) {
        if (!html) {
          return;
        }
        var content = $compile(html)(scope);
        content.insertBefore(elem);
        //$(html).insertBefore(elem);
        //$compile(elem.contents())(scope)
      })
    }
  }
});

myApp.directive('monthtask', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('task.monthtask', function(html) {
        if (!html) {
          return;
        }
        if (attrs.monthtask == scope.task.category_id) {
          var content = $compile(html)(scope);
          content.insertBefore(elem);
          //$(html).insertBefore(elem);
          //$compile(elem.contents())(scope);
        }
      })
    }
  }
});

myApp.directive('weektask', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('task.weektask', function(html) {
        if (!html) {
          return;
        }
        if (attrs.weektask == scope.task.category_id) {
          var content = $compile(html)(scope);
          content.insertBefore(elem);
          //$(html).insertBefore(elem);
          //$compile(elem.contents())(scope);
        }
      })
    }
  }
});

myApp.directive('commtask', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('task.commtask', function(html) {
        if (!html) {
          return;
        }
        if (attrs.commtask == scope.task.category_id) {
          var content = $compile(html)(scope);
          content.insertBefore(elem);
          //$(html).insertBefore(elem);
          //$compile(elem.contents())(scope);

        }
      })
    }
  }
});

myApp.directive('temptask', function($compile) {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      scope.$watch('task.temptask', function(html) {
        if (!html) {
          return;
        }
        var content = $compile(html)(scope);
        content.insertBefore(elem)
      })
    }
  }
});

//var updateCommtasks = function(newCommtasks) {
//  angular.copy(newCommtasks, $scope.commtasks)
//};
//
//updateCommtasks($scope.commtasks);

myApp.directive('commtaskcontent', function() {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      //for (var key in scope.commtasks) {
      angular.forEach(scope.commtasks, function(value, key) {
        scope.$watch('commtasks['+key+'].content', function (newValue, oldValue) {
          if (key == attrs.commtaskcontent && newValue != oldValue) {
            elem.html(newValue);
          }
        }, true)
      });
    }
  }
});

myApp.directive('temptaskcontent', function() {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      angular.forEach(scope.temptasks, function(value, key) {
        scope.$watch('temptasks['+key+'].content', function (newValue, oldValue) {
          if (key == attrs.temptaskcontent && newValue != oldValue) {
            elem.html(newValue);
          }
        }, true)
      });
    }
  }
});

myApp.directive('monthtaskcontent', function() {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      angular.forEach(scope.monthtasks, function(value, key) {
        scope.$watch('monthtasks['+key+'].content', function (newValue, oldValue) {
          if (key == attrs.monthtaskcontent && newValue != oldValue) {
            elem.html(newValue);
          }
        }, true)
      });
    }
  }
});

myApp.directive('weektaskcontent', function() {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      angular.forEach(scope.weektasks, function(value, key) {
        scope.$watch('weektasks['+key+'].content', function (newValue, oldValue) {
          if (key == attrs.weektaskcontent && newValue != oldValue) {
            elem.html(newValue);
          }
        }, true)
      });
    }
  }
});

myApp.directive('commtask-sche-started-at', function() {
  return {
    restrict: 'AEC',
    link: function(scope, elem, attrs) {
      angular.forEach(scope.commtasks, function(value, key) {
        debugger
        scope.$watch('commtasks['+key+'].scheduled_started_at', function (newValue, oldValue) {
          if (key == attrs.commtask-sche-started-at && newValue != oldValue) {
            elem.html(newValue);
          }
        })
      })
    }
  }
});



