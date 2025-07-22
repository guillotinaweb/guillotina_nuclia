from guillotina import configure

configure.permission("nuclia.Predict", "Allow to predict")
configure.grant(role="guillotina.Manager", permission="audit.AccessContent")
